import re
file_path = "input.txt"

ret = 0

values = []

with open(file_path) as file:
    for line in file.readlines():
        values.append(line.strip("\r\n"))
        line = line.strip()
        for i in range(len(line)):
            if line[i].isdigit():
                first_digit = int(line[i])
                break


        for i in range(len(line)-1, -1, -1):
            if line[i].isdigit():
                last_digit = int(line[i])
                break


        number = first_digit*10 + last_digit
        print(number)
        ret += int(number)

print(ret)


# pt 2


ret = 0

digits = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

test = "1|2|3|4|5|6|7|8|9"
test += "|" + "|".join(digits)

for cur in values:
    m = re.search(".*?(" + test + ")", cur)
    val = digits.get(m.group(1), m.group(1))
    m = re.search(".*(" + test + ")", cur)
    val += digits.get(m.group(1), m.group(1))
    ret += int(val)

print(ret)