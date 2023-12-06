import re
file_path = "input.txt"

ll = [x for x in open(file_path).read().strip().split('\n')]
p1 = 0
multiplier = [1 for i in ll]
p2 = 0
for i,l in enumerate(ll):
	winning = set([int(x) for x in l.split(":")[1].split("|")[0].strip().split()])
	have = [int(x) for x in l.split("|")[1].strip().split()]
	have = [x for x in have if x in winning]
	if len(have):
		p1 += 2**(len(have)-1)
	mymult = multiplier[i]
	for j in range(i+1,min(i+len(have)+1,len(ll))):
		multiplier[j]+=mymult
	p2 += mymult
print(p1, p2)
