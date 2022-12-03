import pathlib

def main():
	total1 = 0
	total2 = 0
	priority = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
	content = []
	with open(pathlib.Path("input.txt")) as file:
		for line in file:
			content.append(line)
			first = line[0: len(line)//2]
			second = line[len(line)//2: len(line)]
			for i in first:
				if i in second:
					total1 += priority.index(i) + 1
					break

		for i in range(0, len(content), 3):
			first2 = content[i]
			second2 = content[i + 1]
			third2 = content[i + 2]
			for a in first2:
				if a in second2 and a in third2:
					total2 += priority.index(a) + 1
					break
	print(total1)
	print(total2)

if __name__ == "__main__":
	main()