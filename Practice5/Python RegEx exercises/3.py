import re

# 3. Find sequences of lowercase letters joined with an underscore
text = "hello_world abc_def Test_case one_two_three"
pattern = r"\b[a-z]+_[a-z_]+\b"

print(re.findall(pattern, text))