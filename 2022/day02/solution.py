
import pathlib

def main():
	total = 0
	with open(pathlib.Path("input.txt")) as file:
		for line in file:
			moves = line.split()
			opp = moves[0]
			you = moves[1]
			if (you == "X"):
				total += 1
			if (you == "Y"):
				total += 2
			if (you == "Z"):
				total += 3
			if (you == "X" and opp == "A" or you == "Y" and opp == "B" or you == "Z" and opp == "C"):
				total += 3
			if (opp == "B" and you == "Z" or opp == "A" and you == "Y" or opp == "C" and you == "X"):
				total += 6
	print (total)

def main2():
	total = 0
	with open(pathlib.Path("input.txt")) as file:
		for line in file:
			moves = line.split()
			opp = moves[0]
			you = moves[1]
			if (opp == "A"):
				if(you == "X"):
					total += 3
				if(you == "Y"):
					total += 1
					total += 3
				if(you == "Z"):
					total += 2
					total += 6
			if (opp == "B"):
				if(you == "X"):
					total += 1
				if(you == "Y"):
					total += 2
					total += 3
				if(you == "Z"):
					total += 3
					total += 6
			if (opp == "C"):
				if(you == "X"):
					total += 2
				if(you == "Y"):
					total += 3
					total += 3
				if(you == "Z"):
					total += 1
					total += 6
	print (total)

if __name__ == "__main__":
	main()
	main2()