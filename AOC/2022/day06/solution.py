
import pathlib
import heapq
def main():
	with open(pathlib.Path("input.txt")) as file:
		for line in file:
			for i in range(len(line)-3):
				if (len(set(line[i:i+4])) == len(line[i:i+4])):
					print (i + 4)
					break
			for i in range(len(line)-13):
				if (len(set(line[i:i+14])) == len(line[i:i+14])):
					print (i + 14)
					break

if __name__ == "__main__":
	main()

