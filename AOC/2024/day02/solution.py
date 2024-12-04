import re
with open('input.txt', 'r') as file:
    lines = file.readlines()

data = []
for line in lines:
    report = list(map(int, re.findall(r'\d+', line)))
    data.append(report)

def is_safe_report(report):
    differences = [abs(report[i] - report[i + 1]) for i in range(len(report) - 1)]

    if not all(1 <= diff <= 3 for diff in differences):
        return False
    
    is_increasing = all(report[i] < report[i + 1] for i in range(len(report) - 1))
    is_decreasing = all(report[i] > report[i + 1] for i in range(len(report) - 1))
    
    return is_increasing or is_decreasing

safe_reports_count = sum(is_safe_report(report) for report in data)
print(safe_reports_count)


def is_safe_with_dampener(report):
    if is_safe_report(report):
        return True

    for i in range(len(report)):
        modified_report = report[:i] + report[i + 1:]
        if is_safe_report(modified_report):
            return True

    return False

safe_reports_with_dampener_count = sum(is_safe_with_dampener(report) for report in data)
print(safe_reports_with_dampener_count)