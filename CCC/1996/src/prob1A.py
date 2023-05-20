"""
Problem A: Deficient, Perfect, and Abundant
Input file: dpa.in
Output file: dpa.out

Write a program that repeatedly reads a positive integer, determines if the integer is deficient, perfect, or abundant, and outputs the number along with its classification.

A positive integer, n, is said to be perfect if the sum of its proper divisors equals the number itself. (Proper divisors include 1 but not the number itself.) If this sum is less that n, the number is deficient, and if the sum is greater than n, the number is abundant.

The input starts with the number of integers that follow. For each of the following integers, your program should output the classification, as given below. You may assume that the input integers are greater than 1 and less than 32500.

Sample input
3
4
6
12
Sample output
4 is a deficient number.

6 is a perfect number.

12 is an abundant number.
"""

def func(num: int):
    sum = 0
    for i in range(1, int(num)):
        if (num % i == 0):
            sum += i
    
    if (sum == num):
        return str(num) + " is a perfect number."
    elif (sum < num):
        return str(num) + " is a deficient number."
    else:
        return str(num) + " is an abundant number."


def test(year: str, filename: str):
    path = "CCC/" + str(year) + "/data/" + filename
    in_file = open(path + ".in", "r")
    in_lines = in_file.readlines()
    
    out_file = open(path + ".out", "r")
    out_lines = out_file.readlines()
    for line in out_lines:
        #remove null values from out_linies
        if line == "\n" or line == "":
            out_lines.remove(line)
    
    for i in range(len(in_lines) - 1):
        if func(int(in_lines[i + 1])) == out_lines[i]:
            print("Test case " + str(i) + " passed.")
            print()
        else:
            print("Test case " + str(i) + " failed.")
            print("    Got     : " + func(int(in_lines[i + 1])))
            print("    Expected: " + out_lines[i])
            print()

test(1996, "dpa")
