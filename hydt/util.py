import calendar

from datetime import date, datetime, timedelta
from textblob import TextBlob


def get_text_sentiment(text):
    if not text:
        return 0

    analysis = TextBlob(text)

    return analysis.sentiment.polarity


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


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


def monthrange(month):
    end = calendar.monthrange(month.year, month.month)
    end = date(month=month.month, day=end[1], year=month.year)

    return daterange(month, end)
