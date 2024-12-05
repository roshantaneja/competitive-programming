import re

with open('input.txt', 'r') as file:
    lines = file.read().strip().split("\n\n")


ordering_rules = lines[0].splitlines()
updates = [list(map(int, update.split(','))) for update in lines[1].splitlines()]



graph = {}
for rule in ordering_rules:
    x, y = map(int, rule.split('|'))
    if x not in graph:
        graph[x] = []
    graph[x].append(y)


def is_correct_order(update, rules):
    position = {}
    for idx in range(len(update)):
        position[update[idx]] = idx
    for x in update:
        if x in rules:
            for y in rules[x]:
                if y in position and position[y] < position[x]:
                    return False
    return True


def topological_sort(update, graph):
    in_degree = {page: 0 for page in update}
    subgraph = {page: [] for page in update}
    
    for x in update:
        if x in graph:
            for y in graph[x]:
                if y in update:
                    subgraph[x].append(y)
                    in_degree[y] += 1
    

    queue = [page for page in update if in_degree[page] == 0]
    sorted_update = []
    
    while queue:
        current = queue.pop(0)
        sorted_update.append(current)
        for neighbor in subgraph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return sorted_update

correct_middle_sum = 0
fixed_middle_sum = 0

for update in updates:
    if is_correct_order(update, graph):
        correct_middle_sum += update[len(update) // 2]
    else:
        fixed_update = topological_sort(update, graph)
        fixed_middle_sum += fixed_update[len(fixed_update) // 2]

print(f"Sum of middle pages for correctly ordered updates: {correct_middle_sum}")
print(f"Sum of middle pages for fixed updates: {fixed_middle_sum}")