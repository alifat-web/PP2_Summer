import datetime

date1 = datetime.datetime(2026, 6, 20, 12, 0, 0)
date2 = datetime.datetime(2026, 6, 20, 12, 1, 30)

difference = date2 - date1

print("Difference in seconds:", difference.total_seconds())