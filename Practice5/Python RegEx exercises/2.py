import re

# 2. Match a string that has an 'a' followed by two to three 'b's
text = "abbb"
pattern = r"ab{2,3}"

if re.fullmatch(pattern, text):
    print("Match")
else:
    print("No match")