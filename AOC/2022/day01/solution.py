import heapq
import pathlib

def main():
    with open(pathlib.Path("input.txt")) as file:
        heap = []
        total = 0
        for line in file:
            try:
                total += int(line)
            except ValueError:
                if len(heap) < 3:
                    heapq.heappush(heap, total)
                else:
                    heapq.heappushpop(heap, total)
                total = 0

    print(max(heap))
    print(sum(heap))


if __name__ == "__main__":
    main()