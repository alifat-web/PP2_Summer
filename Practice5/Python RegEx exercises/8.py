import re

# 8. Split a string at uppercase letters
text = "HelloWorldPython"

result = re.split(r"(?=[A-Z])", text)

# Remove the empty string at the beginning
result = [word for word in result if word]

print(result)