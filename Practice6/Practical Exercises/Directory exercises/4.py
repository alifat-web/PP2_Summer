import os
import shutil

os.makedirs("Destination", exist_ok=True)

shutil.copy("sample.txt", "Destination/sample.txt")

print("File copied.")