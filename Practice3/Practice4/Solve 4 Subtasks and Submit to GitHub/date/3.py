import datetime

now = datetime.datetime.now()

without_microseconds = now.replace(microsecond=0)

print("Original:", now)
print("Without microseconds:", without_microseconds)