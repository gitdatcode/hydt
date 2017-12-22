import argparse
import json
import re
import sys
import operator

from datetime import datetime

from .color import COLORS
from .emoji import EMOJI
from .model import create_tables, migrate_tables, User, UserDay
from .config import options
from .util import colorscale, get_text_sentiment


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('command', nargs=1, type=str)
    parser.add_argument('--user', '-u', help='the id for the user', type=int)
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

    try:
        args = parser.parse_args()
        command = args.command[0]
        date = _make_date(args.date)
        start_date = _make_date(args.sdate)
        end_date = _make_date(args.edate)

        if args.emoji:
            emoji = list(map(str.strip, re.split(r'[;,\s]\s*', args.emoji)))
        else:
            emoji = None

        if command == 'score':
            data = get_emoji_data(emoji)
        elif command == 'user_score':
            data = get_user_score(user=args.user, emoji=emoji, date=date,
                notes=args.notes)
            print(data)
        elif command == 'user_score_range':
            data = get_user_score_range(user=args.user, start=start_date,
                end=end_date)
            print(data)
        elif command == 'create_database':
            create_tables()
        elif command == 'migrate':
            migrate_tables()

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
    data = get_emoji_data(emoji)
    user_day.emoji = ','.join(emoji)
    user_day.color = data['color']
    user_day.color_shifted = data['color_shifted']
    user_day.code = data['score']
    user_day.notes = notes
    user_day.sentiment = get_text_sentiment(notes)

    user_day.save()

    return {
        'user': user.slack_id,
        'date': str(date),
        'data': data,
    }


def get_user_score_range(user, start, end):
    user = User.select().where(slack_id=user)
    user_days = (UserDay.select()
        .where(
            (UserDay.user == user),
            (UserDay.day >= start),
            (UserDay.day <= end),
        ))
    data = []

    for day in user_days:
        data.append()

    return {
        'user': user.slack_id,
        'data': data,
    }


def get_emoji_data(emoji):
    score, scores = calculate_score(emoji)
    color = get_color(score)
    color_shifted = get_color_shifted(color, scores)

    return {
        'score': score,
        'color': color,
        'color_shifted': color_shifted,
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

    return score // len(emoji), scores


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
