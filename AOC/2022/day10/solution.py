import pathlib

content = [x for x in open("input.txt").read().strip().split('\n')]
# with open(pathlib.Path("input.txt")) as file:
#     for line in file:
#         content.append(line)

def parse(i):
    if (len(content[i].split()) > 1):
        a, b = content[i].split()
        yield a, int(b)
    else:
        yield content[i], 0



x = 1
count = 0
sum = 0
crt = [["." for x in range(40)] for y in range(6)]
def cycle():
	global count, sum, x
	count += 1
	if count == 20 or count == 60 or count == 100 or count == 140 or count == 180 or count == 220:
		sum += count * x
	if abs((count - 1) % 40 - x) < 2:
		crt[(count - 1) // 40][(count - 1) % 40] = "@"

for line in content:
	if line == "noop":
		cycle()
	else:
		add = int(line[5:])
		cycle()
		cycle()
		x += add

print(sum)
for i in crt:
    print(''.join(i))

# 15120
# ........................................
# @@@..@..@.@@@....@@.@@@..@@@..@.....@@..
# @..@.@.@..@..@....@.@..@.@..@.@....@..@.
# @..@.@@...@..@....@.@@@..@..@.@....@..@. ====================>>>>>>  RKPJBPLA
# @@@..@.@..@@@.....@.@..@.@@@..@....@@@@.
# @.@..@.@..@....@..@.@..@.@....@....@..@.
# @..@.@..@.@.....@@..@@@..@....@@@@.@..@.
