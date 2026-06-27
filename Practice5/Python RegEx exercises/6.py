import re

# 6. Replace spaces, commas, or dots with a colon
text = "Hello, world. Python is fun"
result = re.sub(r"[ ,.]", ":", text)

print(result)