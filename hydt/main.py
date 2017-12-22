import argparse
import json
import re
import sys
from functools import reduce
import operator

from .color import COLORS
from .emoji import EMOJI
from .options import options


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('command', nargs=1, type=str)
    parser.add_argument('--user', '-u', help='the id for the user', type=int)
    parser.add_argument('--date', '-d', help='The date in MM/DD/YYYY format',
        type=str)
    parser.add_argument('--emoji', '-e', help='The emoji to be parsed',
        type=str)

    args = parser.parse_args()
    command = args.command[0]

    if args.emoji:
        emoji = list(map(str.strip, re.split(r'[;,\s]\s*', args.emoji)))
    else:
        emoji = None

    try:
        if command == 'score':
            data = get_emoji_data(emoji)
            print('>>>', data)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(e, file=sys.stderr)


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




def calculate_mood(scores):
    if len(scores) == 1:
        return scores[0]

    changes = []
    print(scores)
    for f, s in zip(scores, scores[1:]):
        print(']]]', f, s)
        score = (((s - f) / f) * f) + f

        changes.append(score)

    print('===', changes)

    # return (sum(changes) / 3) * 100
    return calculate_mood(changes)


def calculate_moodx(scores):
    print('SCORES', scores)
    mood = scores.pop(0)
    new = scores.pop(0)

    while new and mood:
        print('mn', new, mood)
        mood = ((new - abs(mood)) / abs(mood)) * 100
        print('==', mood)
        try:
            new = scores.pop(0)
        except:
            new = None

    return mood


def calculate_moodx(scores):
    if len(scores) == 1:
        return scores[0] / 100

    pairs = []

    for first, second in zip(scores, scores[1:]):
        pairs.append(second - first)

    return calculate_mood(pairs)

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
        percent = (second - first) / second
        color = colorscale(color, percent)

    return color


def clamp(val, minimum=0, maximum=255):
    if val < minimum:
        return minimum

    if val > maximum:
        return maximum

    return val


def colorscale(hexstr, scalefactor):
    """
    Scales a hex string by ``scalefactor``. Returns scaled hex string.

    To darken the color, use a float value between 0 and 1.
    To brighten the color, use a float value greater than 1.

    >>> colorscale("#DF3C3C", .5)
    #6F1E1E
    >>> colorscale("#52D24F", 1.6)
    #83FF7E
    >>> colorscale("#4F75D2", 1)
    #4F75D2
    """

    hexstr = hexstr.strip('#')

    if scalefactor < 0 or len(hexstr) != 6:
        return hexstr

    r, g, b = int(hexstr[:2], 16), int(hexstr[2:4], 16), int(hexstr[4:], 16)
    r = int(clamp(r * scalefactor))
    g = int(clamp(g * scalefactor))
    b = int(clamp(b * scalefactor))

    return "#%02x%02x%02x" % (r, g, b)
