import os

filename = "backup.txt"

if os.path.exists(filename):
    os.remove(filename)
    print("File deleted.")
else:
    print("File does not exist.")