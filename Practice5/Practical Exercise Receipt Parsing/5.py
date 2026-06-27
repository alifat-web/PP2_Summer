import re

with open("Practice5/Practical Exercise Receipt Parsing/raw.txt", "r", encoding="utf-8") as file:
    text = file.read()

match = re.search(r"(.+):[\s\S]*?ИТОГО:", text)

print(match.group(1))
    