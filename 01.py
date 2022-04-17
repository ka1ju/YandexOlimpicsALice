x = int(input())
y = int(input())
z = int(input())
if (x + y + z) % 2 == 1 or x > y + z:
    print("Не получается")
else:
    a = [z - (y + z - x) // 2, 0, z - (y + z - x) // 2]
    b = [0, (y + z - x) // 2, (y + z - x) // 2]
    c = [y - (y + z - x) // 2, y - (y + z - x) // 2, 0]
    print(a[0], a[1], a[2])
    print(b[0], b[1], b[2])
    print(c[0], c[1], c[2])
