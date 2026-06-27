import re

# 5. Match a string that has an 'a' followed by anything, ending in 'b'
text = "a12345b"
pattern = r"a.*b"

if re.fullmatch(pattern, text):
    print("Match")
else:
    print("No match")