import secrets

def randbits(k):
    return secrets.randbits(k)

def gcd(a, b):
    if a == 0:
        return b
    if b == 0:
        return a
    return gcd(b, a%b)

class factors:
    class factor_generator:
        def __init__(self, n):
            self.n = n

class primes:
    @staticmethod
    def maybe_prime(self, p, trials=16):
        if p % 2 == 0:
            return False
        # find k and m
        k, m = 1, None
        tmp = (p - 1) / (2 ** k)
        while tmp % 1 == 0:
            m = int(tmp)
            k += 1
            tmp = (p - 1) / (2 ** k)
        k -= 1
        # test
        a = secrets.randbelow(p - 1) + 1

    @staticmethod
    def is_prime(self, n):
        pass

def randprime(m=2048):
    pp = randbits(m)
    
