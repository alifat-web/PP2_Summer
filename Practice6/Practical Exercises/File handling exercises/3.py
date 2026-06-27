with open("sample.txt", "a") as file:
    file.write("David\n")
    file.write("Emma\n")

print("New lines added.\n")

with open("sample.txt", "r") as file:
    print(file.read())