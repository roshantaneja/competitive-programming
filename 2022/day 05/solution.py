import pandas as pd

stacks = pd.read_fwf('input2.txt', header=None)
from collections import deque

myres = {}
for col in stacks.columns:
    myres[col + 1] = deque(stacks[col].dropna())

df = pd.read_csv('input.txt', sep=' ', header=None)

df.columns = ['x', 'quantity', 'xx', 'source', 'xxx', 'dest']

commands = df.to_dict('records')

for command in commands:
    for i in range(0, command['quantity']):
        package = myres[command['source']].popleft()
        myres[command['dest']].appendleft(package)

print(''.join([x[0][1] for x in myres.values()]))

df = pd.read_csv('input.txt', sep=' ', header=None)
df.columns = ['x', 'quantity', 'xx', 'source', 'xxx', 'dest']
myres = {}
for col in stacks.columns:
    myres[col + 1] = deque(stacks[col].dropna())

for command in commands:
    packages = []
    for i in range(0, command['quantity']):
        package = myres[command['source']].popleft()
        packages.append(package)
    packages.reverse()
    for p in packages:
        myres[command['dest']].appendleft(p)
print(''.join([x[0][1] for x in myres.values()]))

#MQSHJMWNH
#LLWJRBHVZ