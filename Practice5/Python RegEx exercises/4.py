import re

# 4. Find sequences of one uppercase letter followed by lowercase letters
text = "Hello World ABC Python"
pattern = r"\b[A-Z][a-z]+\b"

print(re.findall(pattern, text))