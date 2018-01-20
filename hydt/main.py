import argparse
import calendar
import json
import re
import sys
import operator
import os
import errno

from collections import OrderedDict
from datetime import datetime, timedelta, date

from tornado import template

from .color import COLORS
from .emoji import EMOJI
from .model import create_tables, migrate_tables, User, UserDay
from .config import options
from .util import colorscale, get_text_sentiment, daterange, monthrange


NOW = datetime.now()
WEEK = NOW.isocalendar()[1]
JAN_1 = datetime(day=1, month=1, year=NOW.year).date()
DEC_31 = datetime(day=31, month=12, year=NOW.year).date()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('command', nargs=1, type=str)
    parser.add_argument('--user', '-u', help='the id for the user', type=str)
    parser.add_argument('--date', '-d', help='The date in MM/DD/YYYY format',
        type=str)
    parser.add_argument('--sdate', '-sd',
        help='The start date in MM/DD/YYYY format', type=str)
    parser.add_argument('--edate', '-ed',
        help='The end date in MM/DD/YYYY format', type=str)
    parser.add_argument('--emoji', '-e', help='The emoji to be parsed',
        type=str)
    parser.add_argument('--notes', '-n',
        help='Any notes to go along with the entry', type=str)
    parser.add_argument('--year', '-y', default=NOW.year, help='The year')
    parser.add_argument('--week', '-w', default=WEEK, help='The week')


    try:
        data = {}
        args = parser.parse_args()
        command = args.command[0]
        date = _make_date(args.date)
        start_date = _make_date(args.sdate)
        end_date = _make_date(args.edate)

        if args.emoji:
            emoji = list(map(str.strip, re.split(r'[;,\s]\s*', args.emoji)))
        else:
            emoji = None

        if command == 'emoji':
            data = EMOJI
        elif command == 'colors':
            data = COLORS
        elif command == 'score':
            data = get_emoji_data(emoji)
        elif command == 'user_score':
            data = get_user_score(user=args.user, emoji=emoji, date=date,
                notes=args.notes)
        elif command == 'user_score_range':
            data = get_user_score_range(user=args.user, start=start_date,
                end=end_date)
        elif command == 'generate_week':
            file_name = generate_week_template(user=args.user, week=args.week,
                year=args.year)
            data = {'file_name': file_name}
        elif command == 'create_database':
            create_tables()
        elif command == 'migrate':
            migrate_tables()

        print(json.dumps(data))
    except Exception as e:
        print(e, file=sys.stderr)


def _make_date(date):
    if date:
        if 2 == 3:
            raise Exception('The date format must be "mm/dd/yyyy"')

        return datetime.strptime(date, '%m/%d/%Y').date()

    return None


def get_user_score(user, emoji, date, notes=None):
    if not user or not emoji or not date:
        raise Exception('Must pass in a user - u, emoji -e, and date -d')

    user, _ = User.get_or_create(slack_id=user)
    user_day, _ = UserDay.get_or_create(user=user, day=date)
    data = get_emoji_data(emoji, notes)
    user_day.emoji = ','.join(emoji)
    user_day.color = data['color']
    user_day.color_shifted = data['color_shifted']
    user_day.code = data['score']
    user_day.notes = notes
    user_day.sentiment = data['sentiment']

    user_day.save()

    return {
        'user': user.slack_id,
        'date': str(date),
        'data': data,
    }


def get_user_score_range(user, start, end):
    """returns the user data for a given date range will be in the format of

        {
            'user': user.id<String>,
            'date': {
            
            },
            'data': {
                year<Int>: {
                    month<Int>: {
                        day<Int>: {
                            'score': <Float>,
                            'emoji': <String>,
                            'notes': <String>,
                            'color': <String>,
                            'color_shifted': <String>,
                            'sentiment': <Float>,
                        }
                    }
                }
            }
        }
    """
    user = User.select().where(User.slack_id == user).get()
    data = OrderedDict()

    for d in daterange(start, end):
        month_year = d.strftime('%m_%Y')

        if d.year not in data:
            data[d.year] = OrderedDict()

        if d.month not in data[d.year]:
            data[d.year][d.month] = OrderedDict()

        if d.day not in data[d.year][d.month]:
            try:
                if not isinstance(d, date):
                    d = datetime.date()

                user_day = (UserDay.select()
                    .where(
                        (UserDay.user == user),
                        (UserDay.day == d),
                    ).get())
                day_data = user_day.data
            except Exception as e:
                day_data = {}

            data[d.year][d.month][d.day] = day_data

    return {
        'date': {
            'start': start.strftime('%m/%d/%Y'),
            'end': end.strftime('%m/%d/%Y'),
        },
        'user': user.slack_id,
        'data': data,
    }


def get_emoji_data(emoji, notes=None):
    score, scores = calculate_score(emoji)
    color = get_color(score)
    color_shifted = get_color_shifted(color, scores)
    sentiment = get_text_sentiment(notes)

    return {
        'score': score,
        'color': color,
        'color_shifted': color_shifted,
        'sentiment': sentiment,
    }


def calculate_score(emoji):
    score = 0
    scores = []

    for e in emoji:
        val = EMOJI.get(e, None)

        if not val:
            raise Exception('{} is not a supported emoji'.format(e))

        score += val
        scores.append(val)

    return score / len(emoji), scores


def get_color(score, shift=None):
    score = float(score)

    for val, color in COLORS.items():
        if score <= val:
            return color

    raise Exception('Score not found: {}'.format(score))


def get_color_shifted(color, scores):
    scores = [v for i, v in enumerate(scores) if i == 0 or v != scores[i-1]]

    if len(scores) == 1:
        return color

    for first, second in zip(scores, scores[1:]):
        percent = abs((second - first) / first)

        if percent >= .01:
            color = colorscale(color, percent)

    return color


def generate_week_template(user, week=WEEK, year=NOW.year):
    # templates
    loader = template.Loader(options.template_path, autoescape=None)
    overview_template = loader.load('report/month/overview.html')
    month_template = loader.load('report/month/month.html')
    month_day_template = loader.load('report/month/day.html')
    week_template = loader.load('report/week/week.html')
    week_day_template = loader.load('report/week/day.html')
    report_template = loader.load('report/report.html')

    # data
    week_start = datetime.strptime('{}W{} MON'.format(year, week), '%YW%U %a')
    week_end = week_start + timedelta(days=6)
    week_data = get_user_score_range(user=user, start=week_start.date(),
        end=week_end.date())
    year_data = get_user_score_range(user=user, start=JAN_1, end=DEC_31)
    cal_months = []

    def calendar_month(month, year, data):
        end = calendar.monthrange(year, month)
        month = date(month=month, year=year, day=1)

        return (month_template.generate(month=month, last_month_day=end[1],
            monthrange=monthrange, month_day_template=month_day_template,
            data=data, autoescape=False).decode('utf-8'))

    for month, data in year_data['data'][year].items():
        cal_months.append(calendar_month(month=month, year=year, data=data))

    week_content = week_template.generate(week=week,
        data=week_data['data'][year][week_start.month],
        week_day_template=week_day_template).decode('utf-8')
    months = overview_template.generate(months=cal_months, year=year)
    report = report_template.generate(months=months, week=week_content,
        autoescape=False).decode('utf-8')
    file_name = '{dir}/{user}/{year}/{week}.html'.format(
        dir=options.report_save_directory, user=user, year=year, week=week)

    # save the file
    if not os.path.exists(os.path.dirname(file_name)):
        try:
            os.makedirs(os.path.dirname(file_name))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(file_name, 'w') as f:
        f.write(report)

    return file_name
