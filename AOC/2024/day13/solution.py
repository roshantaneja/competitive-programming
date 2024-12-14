with open("input.txt") as file:
    raw_lines = file.read().strip().split('\n')

lines = [l.strip() for l in raw_lines if l.strip()]
if len(lines) % 3 != 0:
    raise ValueError("Input lines are not a multiple of 3. Check input format.")

machines = []
i = 0
while i < len(lines):
    lineA = lines[i].strip()
    lineB = lines[i+1].strip()
    lineC = lines[i+2].strip()
    i += 3

    partA = lineA.split(':', 1)[1].strip()
    xa_str, ya_str = [p.strip() for p in partA.split(',')]
    xA = int(xa_str.replace('X','').strip('+'))
    yA = int(ya_str.replace('Y','').strip('+'))

    partB = lineB.split(':', 1)[1].strip()
    xb_str, yb_str = [p.strip() for p in partB.split(',')]
    xB = int(xb_str.replace('X','').strip('+'))
    yB = int(yb_str.replace('Y','').strip('+'))

    partC = lineC.split(':', 1)[1].strip()
    xC_str, yC_str = [p.strip() for p in partC.split(',')]
    targetX = int(xC_str.replace('X=',''))
    targetY = int(yC_str.replace('Y=',''))

    machines.append((xA, yA, xB, yB, targetX, targetY))

def part1():
    solvable_costs = []
    for (xA, yA, xB, yB, targetX, targetY) in machines:
        min_cost = None
        for A in range(100):
            if xB != 0:
                if (targetX - A*xA) % xB != 0:
                    continue
                B_candidate = (targetX - A*xA)//xB
            else:
                if targetX != A*xA:
                    continue
                B_candidate = None

            if yB != 0:
                if (targetY - A*yA) % yB != 0:
                    continue
                B_from_y = (targetY - A*yA)//yB
            else:
                if targetY != A*yA:
                    continue
                B_from_y = 0

            if B_candidate is None:
                B_candidate = B_from_y

            if yB != 0 and B_candidate != B_from_y:
                continue

            B = B_candidate
            if 0 <= B <= 100:
                cost = 3*A + B
                if min_cost is None or cost < min_cost:
                    min_cost = cost

        if min_cost is not None:
            solvable_costs.append(min_cost)

    max_prizes = len(solvable_costs)
    total_tokens = sum(solvable_costs)
    return(max_prizes, total_tokens)

def part2():
    OFFSET = 10_000_000_000_000
    solvable_costs = []
    for (xA, yA, xB, yB, origX, origY) in machines:
        targetX = origX + OFFSET
        targetY = origY + OFFSET
        det = xA*yB - yA*xB

        if det == 0:
            continue
        else:
            numA = targetX*yB - targetY*xB
            numB = targetY*xA - targetX*yA

            if numA % det != 0 or numB % det != 0:
                continue

            A = numA // det
            B = numB // det

            if A < 0 or B < 0:
                continue

            cost = 3*A + B
            solvable_costs.append(cost)

    max_prizes = len(solvable_costs)
    total_tokens = sum(solvable_costs)
    return(max_prizes, total_tokens)


print("Part 1:", part1())
print("Part 2:", part2())


