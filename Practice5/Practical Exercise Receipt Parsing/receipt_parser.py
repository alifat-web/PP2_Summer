import re
import json

with open("Practice5/Practical Exercise Receipt Parsing/raw.txt", "r", encoding="utf-8") as file:
    text = file.read()

prices = re.findall(r"Стоимость\n([^\n]+)", text)

products = re.findall(r"\d+\.\n(.*?)\n\d+,\d+\s*x", text)

total = re.findall(r"\bИТОГО:[\n](\w.*)", text)

date_time = re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})", text)

payment = re.search(r"(.+):[\s\S]*?ИТОГО:", text)

data = {
    "prices": prices,
    "products": products,
    "total_amount": f"{total}",
    "date": date_time.group(1),
    "time": date_time.group(2),
    "payment_method": payment.group(1)
}

with open("output.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(json.dumps(data, ensure_ascii=False, indent=4))