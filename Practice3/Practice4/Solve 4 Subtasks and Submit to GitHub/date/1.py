import datetime

today = datetime.datetime.now()
five_days_ago = today - datetime.timedelta(days=5)

print("Today:", today)
print("Five days ago:", five_days_ago)