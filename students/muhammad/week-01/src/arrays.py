a = [x ** 2 for x in range(0, 21, 2)]
print(a)

########################################################

helper_arr = [[1, 2, 3], [1, 2], [1], [1, 2, 3, 4]]
b = []

for subarr in helper_arr:
    for ele in subarr:
        b.append(ele)

print(b)

########################################################


