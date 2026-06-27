import re

# 1. Match a string that has an 'a' followed by zero or more 'b's
text = "abbb"
pattern = r"ab*"

if re.findall(pattern, text):
    print("Match")
else:
    print("No match")