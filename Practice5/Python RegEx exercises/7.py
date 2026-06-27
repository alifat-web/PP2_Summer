import re

# 7. Convert snake_case to camelCase
text = "my_python_program"

def snake_to_camel(match):
    return match.group(1).upper()

result = re.sub(r"_([a-z])", snake_to_camel, text)

print(result)