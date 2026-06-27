import re

with open("Practice5/Practical Exercise Receipt Parsing/raw.txt", "r", encoding="utf-8") as file:
    text = file.read()

matches = re.findall(r"Стоимость\s+(\d+)", text)

print(matches)