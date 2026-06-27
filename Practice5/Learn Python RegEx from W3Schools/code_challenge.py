# Import re
import re
# Create a string
txt = "The rain in Spain"
# Search for "Spain"
match = re.search(r"\bSpain", txt)
# Print the span
print(match.span())