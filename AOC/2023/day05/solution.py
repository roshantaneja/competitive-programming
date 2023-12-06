# import re
# import itertools
# from collections import defaultdict
# from pprint import pprint
# from itertools import count
#
# file_path = "input.txt"
#
# ll = [x for x in open(file_path)]
#
# seeds = ll[0].split()[1:]

from functools import reduce

seeds, *maps = open('input.txt').read().split('\n\n')

def lookup(value, m):
    _, *ranges = m.split('\n')
    #print(ranges)
    for r in ranges:
        distance, source, n = map(int, r.split())
        if source <= value < source+n:
            return value-source+distance
    else:
        return value

print(min(reduce(lookup, maps, int(s))for s in seeds.split()[1:]))


newSeeds = seeds.split()[1:]
