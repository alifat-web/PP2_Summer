def even_numbers(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield str(i)

n = int(input("Enter N: "))

for even in even_numbers(n):
    print(even, end=' ')