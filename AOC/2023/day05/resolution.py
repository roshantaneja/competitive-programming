import sys
from datetime import datetime


class Mapping:
    def __init__(self, source: int, dest: int, length: int):
        self.source = source
        self.dest = dest
        self.length = length

    def map(self, source: int) -> int | None:
        diff = source - self.source
        if diff >= 0 and diff < self.length:
            return self.dest + diff
        return None

    def map_range(self, source: tuple[int, int]):
        before, mapped, after = None, None, None
        start, end = self.source, self.source + self.length - 1
        if start > source[0]:
            before = (source[0], min(source[1], start - 1))
        if start <= source[1] and end >= source[0]:
            mapped = (self.map(max(source[0], start)), self.map(min(source[1], end)))
        if end < source[1]:
            after = (max(source[0], end + 1), source[1])
        return (before, mapped, after)


class MappingList:
    def __init__(self, mappings: list[Mapping]):
        self.mappings = mappings

    def map(self, source: int) -> int:
        for m in self.mappings:
            v = m.map(source)
            if v is not None:
                return v
        return source

    def map_range(self, source: tuple[int, int]) -> list[tuple[int, int]]:
        result = []
        toMap = [source]
        for m in self.mappings:
            next = []
            for tm in toMap:
                before, mapped, after = m.map_range(tm)
                if before:
                    next.append(before)
                if mapped:
                    result.append(mapped)
                if after:
                    next.append(after)
            toMap = next
        result.extend(toMap)  # include any last ranges that didn't get mapped
        return result


def parse_seeds(line: str) -> list[int]:
    return [int(s) for s in line.split()[1:]]


def parse_mapping(line: str) -> Mapping:
    dest, source, length = line.split()
    return Mapping(int(source), int(dest), int(length))


def parse_mappings(mstr: str) -> MappingList:
    return MappingList([parse_mapping(m) for m in mstr.split('\n')[1:]])  # skip first line, it's text


def parse_input(parts: list[str]):
    seeds, *mappings = parts
    seeds = parse_seeds(seeds)
    return seeds, [parse_mappings(m) for m in mappings]


def part1(parts: list[str]):
    seeds, mappings = parse_input(parts)
    locations = []
    for seed in seeds:
        val = seed
        for m in mappings:
            val = m.map(val)
        locations.append(val)

    print('Part 1:', min(locations))


def part2(parts: list[str]):
    seedPairs, mappings = parse_input(parts)
    locations = []
    # seeds are ranges, instead of individual seeds now
    seedPairs = zip(seedPairs[::2], seedPairs[1::2])
    for pair in seedPairs:
        seedRanges = [(pair[0], pair[0] + pair[1] - 1)]
        for m in mappings:
            next = []
            for sr in seedRanges:
                # when a range is mapped, you can get a list of ranges back
                next += m.map_range(sr)
            seedRanges = next
            next = []
        locations.append(min(seedRanges)[0])  # take the beginning of min range as the lowest location

    print('Part 2:', min(locations))


if __name__ == '__main__':
    start = datetime.now()
    with open("input.txt") as file:
        parts = file.read().split('\n\n')
    part1(parts)
    part2(parts)
    elapsed = datetime.now() - start
    print("Elapsed time: ", elapsed.microseconds, "us")