import pathlib
import os

i = 0
curdir = None
dirs = {}
subdirs = {}
content = []

with open(pathlib.Path("input.txt")) as file:
    for line in file:
        content.append(line)

for line in content:
    if line[0] == "$":
        c, cmd, *args = line.split()
        if cmd == "cd":
            path ,= args
            if path[0] == "/":
                curdir = path
            else:
                curdir = os.path.normpath(os.path.join(curdir, path))
            if curdir not in dirs:
                dirs[curdir] = 0
                subdirs[curdir] = []
    else:
        sz, fname = line.split()
        if sz != "dir":
            dirs[curdir] += int(sz)
        else:
            subdirs[curdir].append(os.path.normpath(os.path.join(curdir, fname)))

dirSizes = {}
def dirsize(dirName):
    dsize = dirs[dirName]
    for i in subdirs[dirName]:
        dsize += dirsize(i)
    return dsize

totsize = 0

#part 1
for d in dirs:
    dsize = dirsize(d)
    if dsize <= 100000:
        totsize += dsize
print(totsize)

# part 2
totsize = dirsize("/")
unused = 70000000 - totsize
champ = None
for d in dirs:
    dsize = dirsize(d)
    if unused + dsize >= 30000000:
        if champ is None or champ > dsize:
            champ = dsize
print(champ)


