MOD = 16777216  # 2^24

def next_secret_number(secret):
    """
    Compute the next secret number from the given secret, following the 3-step process:
    
    1) Multiply by 64 -> XOR into secret -> mod 2^24
    2) Floor divide by 32 -> XOR into secret -> mod 2^24
    3) Multiply by 2048 -> XOR into secret -> mod 2^24
    """
    # Step 1
    val = secret * 64
    secret ^= val
    secret %= MOD

    # Step 2
    val = secret // 32
    secret ^= val
    secret %= MOD

    # Step 3
    val = secret * 2048
    secret ^= val
    secret %= MOD

    print(secret)

    return secret

def part1():
    with open("input.txt") as f:
        buyers = [int(line.strip()) for line in f if line.strip()]
        
    sum_of_2000th = 0
    for init_secret in buyers:
        secret = init_secret
        for _ in range(2000):
            secret = next_secret_number(secret)
        sum_of_2000th += secret

    return sum_of_2000th

if __name__ == "__main__":
    answer = part1()
    print(answer)