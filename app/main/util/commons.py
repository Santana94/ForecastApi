from datetime import datetime


def convert_datetime(date):
    return datetime.strptime(date, '%Y-%m-%d')
