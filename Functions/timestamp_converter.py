from datetime import datetime
from math import floor


def convert_timestamp(data, mode='R'):
    # +---+---------------------------------------------+---------------------------------------+
    # | t | короткое время                              | 00:00                                 |
    # +---+---------------------------------------------+---------------------------------------+
    # | T | длинное время                               | 00:00:00                              |
    # +---+---------------------------------------------+---------------------------------------+
    # | d | короткая дата                               | 01.01.2023                            |
    # +---+---------------------------------------------+---------------------------------------+
    # | D | длинная дата                                | 1 января 2023 г.                      |
    # +---+---------------------------------------------+---------------------------------------+
    # | f | длинная дата & короткое время               | 1 января 2023 г. в 00:00              |
    # +---+---------------------------------------------+---------------------------------------+
    # | F | длинная дата & день недели & короткое время | воскресенье, 1 января 2023 г. в 00:00 |
    # +---+---------------------------------------------+---------------------------------------+
    # | R | отсчёт                                      | через месяц                           |
    # +---+---------------------------------------------+---------------------------------------+

    if ' ' in data:
        date = data.split(' ')[0]
        time = data.split(' ')[1]

    else:
        if ('-' in data or '.' in data) and not ':' in data:
            date = data
            time = '00:00:00'

        elif ':' in data and not ('-' in data or '.' in data):
            time = data
            date = str(datetime.now().day) + '-' + str(
                datetime.now().month) + '-' + str(datetime.now().year)

    if '-' in date:
        date = date.split('-')

    elif '.' in date:
        date = date.split('.')

    else:
        date = [date]

    if ':' in time:
        time = time.split(':')

    else:
        time = [time]

    if len(date) == 3:
        day = date[0]
        month = date[1]
        year = date[2]

    elif len(date) == 2:
        day = date[0]
        month = date[1]
        year = datetime.now().year

    elif len(date) == 1:
        day = date[0]
        month = datetime.now().month
        year = datetime.now().year

    else:
        raise TypeError('Unknown Date')

    if len(time) == 3:
        hour = time[0]
        minute = time[1]
        second = time[2]

    elif len(time) == 2:
        hour = time[0]
        minute = time[1]
        second = datetime.now().second

    elif len(time) == 1:
        hour = time[0]
        minute = datetime.now().minute
        second = datetime.now().second

    else:
        raise TypeError('Unknown Time')

    timestamp = datetime(year=int(year),
                         month=int(month),
                         day=int(day),
                         hour=int(hour),
                         minute=int(minute),
                         second=int(second)).timestamp()

    timestamp = floor(timestamp)
    return f'<t:{timestamp}:{mode}>'