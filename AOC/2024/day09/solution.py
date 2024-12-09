with open("input1.txt") as file:
    line = file.read().strip()

# Parse the disk map into a list of blocks
def parse_disk(line):
    blocks = []
    file_id = 0
    is_file = True
    i = 0
    while i < len(line):
        length = int(line[i])
        if is_file and length > 0:
            for _ in range(length):
                blocks.append(str(file_id))
            file_id += 1
        elif not is_file and length > 0:
            for _ in range(length):
                blocks.append('.')
        is_file = not is_file
        i += 1
    print(''.join(blocks))
    return blocks

# Compute checksum
def compute_checksum(blocks):
    checksum = 0
    for i, b in enumerate(blocks):
        if b != '.':
            checksum += i * int(b)
    return checksum

# Part 1: Compact by moving individual blocks
def compact_individual(blocks):
    while True:
        try:
            gap_index = blocks.index('.')
        except ValueError:
            break
        rightmost_file = -1
        for i in range(len(blocks) - 1, -1, -1):
            if blocks[i] != '.':
                rightmost_file = i
                break
        if rightmost_file < gap_index:
            break
        blocks[gap_index], blocks[rightmost_file] = blocks[rightmost_file], '.'
    return blocks

# Part 2: Compact by moving whole files
def compact_whole_files(blocks):
    files = {}
    for idx, b in enumerate(blocks):
        if b != '.':
            fid = int(b)
            if fid not in files:
                files[fid] = []
            files[fid].append(idx)

    for fid in sorted(files.keys(), reverse=True):
        file_positions = files[fid]
        file_len = len(file_positions)
        leftmost_file_pos = min(file_positions)
        candidate_start = None
        count = 0
        best_start = None
        for idx in range(0, leftmost_file_pos):
            if blocks[idx] == '.':
                if candidate_start is None:
                    candidate_start = idx
                    count = 1
                else:
                    count += 1
                if count == file_len:
                    best_start = candidate_start
                    break
            else:
                candidate_start = None
                count = 0

        if best_start is not None:
            for pos in file_positions:
                blocks[pos] = '.'
            for offset in range(file_len):
                blocks[best_start + offset] = str(fid)
            files[fid] = list(range(best_start, best_start + file_len))

    return blocks

# Parse the disk map
original_blocks = parse_disk(line)

# Part 1
blocks_part1 = original_blocks[:]
blocks_part1 = compact_individual(blocks_part1)
checksum_part1 = compute_checksum(blocks_part1)

# Part 2
blocks_part2 = original_blocks[:]
blocks_part2 = compact_whole_files(blocks_part2)
checksum_part2 = compute_checksum(blocks_part2)

# Print results
print(checksum_part1)
print(checksum_part2)