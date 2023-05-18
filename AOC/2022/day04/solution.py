
import pathlib

def main():
	total1 = 0
	total2 = 0
	with open(pathlib.Path("input.txt")) as file:
		content = []
		for line in file:
			content.append(line)

		for line in content:
			first = int(line.split(",")[0].split("-")[0])
			second = int(line.split(",")[0].split("-")[1])
			third = int(line.split(",")[1].split("-")[0])
			fourth = int(line.split(",")[1].split("-")[1])

			print(first, second, third, fourth)
			print()

			if (first >= third and second <= fourth) or (first <= third and second >= fourth) : #or (first >= third and first <= fourth) or (second >= third and second <= fourth)
				total1 += 1

			if (first >= third and second <= fourth) or (first <= third and second >= fourth) or (first >= third and first <= fourth) or (second >= third and second <= fourth):
				total2 += 1
	print(total1)
	print(total2)

if __name__ == "__main__":
	main()