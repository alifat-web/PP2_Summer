import re

# 10. Convert camelCase to snake_case
text = "myPythonProgram"

result = re.sub(r"([A-Z])", r"_\1", text).lower()

print(result)