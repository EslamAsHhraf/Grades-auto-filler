def transform(a = 2):
    if a == 1:
        return a + 2
    return a

total = 1

for x in [3,5,1]:
    print(transform(x))
    total = total + transform(x)

print(total)