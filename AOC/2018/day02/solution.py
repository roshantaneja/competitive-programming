import itertools
data = [str(x) for x in open("input.txt").readlines()]

num2 = 0
num3 = 0

for i in data:
    seen = set(i)
    count2 = 0
    count3 = 0
    for letter in seen:
        if i.count(letter) == 2 and count2 == 0:
            num2 += 1
            count2 += 1
        if i.count(letter) == 3 and count3 == 0:
            num3 += 1
            count3 += 1

print(num2 * num3)

#pt 2

#will continue later