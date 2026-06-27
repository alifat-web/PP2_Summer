import re

# 9. Insert spaces between words starting with capital letters
text = "HelloWorldPython"

result = re.sub(r"([A-Z])", r" \1", text).strip()

print(result)