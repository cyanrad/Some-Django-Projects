import datetime


def isRadwansBirthDay():
    today = datetime.date.today()
    return today.day == 21 and today.month == 3
