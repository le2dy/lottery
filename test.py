a = [[10], [0], [-123]]
b = a[0][0] + a[2][0]
d = [10, 1, 2, 1, 5, 6]

c = ['asd', 'qwe', 'asd']

print(d[0] + d[2])
d.insert(1, 12383810)
print(d)

print(sum(d))

indices = [i for i, x in enumerate(c) if x == 'asd']

print(indices)

print(b)
