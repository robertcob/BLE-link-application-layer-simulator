from random import randint
from random import randrange

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def randomHeartRateValue():
    return randrange(60, 100)