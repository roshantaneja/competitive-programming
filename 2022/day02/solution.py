
import pathlib

def main():
	total1 = 0
	total2 = 0
	with open(pathlib.Path("input.txt")) as file:
		for line in file:
			moves = line.split()
			opp = moves[0]
			you = moves[1]
			if (opp == "A"):
				if (you == "X"):
					total1 += 3
					total2 += 3
					total1 += 1
				if (you == "Y"):
					total2 += 1
					total1 += 6
					total1 += 2
					total2 += 3
				if (you == "Z"):
					total2 += 2
					total1 += 3
					total2 += 6
			if (opp == "B"):
				if (you == "X"):
					total2 += 1
					total1 += 1
				if (you == "Y"):
					total1 += 3
					total2 += 2
					total1 += 2
					total2 += 3
				if (you == "Z"):
					total2 += 3
					total1 += 6
					total1 += 3
					total2 += 6
			if (opp == "C"):
				if (you == "X"):
					total2 += 2
					total1 += 6
					total1 += 1
				if (you == "Y"):
					total2 += 3
					total1 += 2
					total2 += 3
				if (you == "Z"):
					total1 += 3
					total2 += 1
					total1 += 3
					total2 += 6
		print(total1)
		print(total2)

if __name__ == "__main__":
	main()