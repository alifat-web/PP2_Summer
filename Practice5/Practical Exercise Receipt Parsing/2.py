import re

with open("Practice5/Practical Exercise Receipt Parsing/raw.txt", "r", encoding="utf-8") as file:
    text = file.read()

matches = re.findall(r"\b(?:[0-9]|1[0-9])\.\s.*?(\w.*)", text)

print(matches)