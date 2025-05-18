def is_prime(n):
    """Check if a number is prime"""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    w = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += w
        w = 6 - w
    return True

def generate_prime_greater_than(n):
    """Generate the smallest prime greater than n"""
    candidate = n + 1
    while True:
        if is_prime(candidate):
            return candidate
        candidate += 1

def is_composite(n):
    """Check if a number is composite"""
    return n > 1 and not is_prime(n)