import math
import random

# number of checks
noc = 10


# l - number of bits
def Gen(l):
    p, q = GenPrime(l), GenPrime(l)
    n = p * q
    # Carmichael function
    fn = (p - 1) * (q - 1)
    if n % 8 == 0:
        fn = int(0.5 * fn)
    while True:
        e = random.randrange(3, fn - 1, 2)
        if math.gcd(e, (p - 1) * (q - 1)) == 1:
            break
    d = ExEu(e, fn)
    return n, e, d, p, q


def GenPrime(l):
    while True:
        n = random.randint(2 ** (l - 1), (2 ** l) - 1)
        if n % 2 == 0:
            continue
        if IsPrime(n):
            return n


def IsPrime(n):
    for _ in range(noc):
        if not SolovayStrassen(n):
            return False
    return True


# Fermat's primality test
def Fermat(n):
    a = random.randint(1, n - 1)
    if math.gcd(a, n) != 1:
        return False
    if ModPow(a, n - 1, n) != 1:
        return False
    return True


# Miller–Rabin's primality test
def MillerRabin(n):
    a = random.randint(1, n - 1)
    if math.gcd(a, n) != 1:
        return False
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    v = ModPow(a, s, n)
    if v % n == 1 or v % n == n - 1:
        return True
    for _ in range(r):
        if v % n == -1:
            return True
        v = (v * v) % n
    return False


# Solovay–Strassen's primality test
def SolovayStrassen(n):
    a = random.randint(1, n - 1)
    if math.gcd(a, n) != 1:
        return False
    if ModPow(a, (n - 1) // 2, n) == JacobiSymbol(a, n):
        return True
    return False


# Calculating the Jacobi symbol
def JacobiSymbol(a, b):
    r = 1
    if a < 0:
        a = -a
        if b % 4 == 3:
            r = -r
    while True:
        t = 0
        while a % 2 == 0:
            t += 1
            a //= 2
        if t % 2 == 1:
            if b % 8 == 3 or b % 8 == 5:
                r = -r
        if a % 4 == b % 4 == 3:
            r = -r
        a, b = b % a, a
        if a == 0:
            return r


class Montgomery:
    def __init__(self, mod):
        self.mod = mod

        self.reducerbits = (mod.bit_length() // 8 + 1) * 8
        self.reducer = 1 << self.reducerbits
        self.mask = self.reducer - 1

        self.reciprocal = ExEu(self.reducer % mod, mod)
        self.factor = (self.reducer * self.reciprocal - 1) // mod
        self.convertedone = self.reducer % mod

    def convert_in(self, x):
        return (x << self.reducerbits) % self.mod

    def convert_out(self, x):
        return (x * self.reciprocal) % self.mod

    def multiply(self, x, y):
        mod = self.mod
        product = x * y
        temp = ((product & self.mask) * self.factor) & self.mask
        reduced = (product + temp * mod) >> self.reducerbits
        result = reduced if (reduced < mod) else (reduced - mod)
        return result

    def pow(self, x, y):
        z = self.convertedone
        while y != 0:
            if y & 1 != 0:
                z = self.multiply(z, x)
            x = self.multiply(x, x)
            y >>= 1
        return z


# Montgomery's reduction algorithm
def ModPow(a, b, MOD):
    mont = Montgomery(MOD)
    u = mont.convert_in(a)
    v = mont.pow(u, b)
    return mont.convert_out(v)


# Extended Euclidean algorithm
def ExEu(e, fn):
    q, r0, r1, x0, x1, y0, y1 = 0, fn, e, 1, 0, 0, 1
    while r1 != 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    if y0 < 0:
        y0 = (y0 + fn) % fn
    return y0


# Encryption
def Encr(msg, e, n):
    encrypted_msg = ModPow(msg, e, n)
    return encrypted_msg


# Decryption using the Chinese remainder theorem
def Decr(msg, d, p, q):
    decr_p = ModPow(msg % p, d % (p - 1), p)
    decr_q = ModPow(msg % q, d % (q - 1), q)
    decr_msg = int((q * decr_p - p * decr_q) // (q - p))
    return decr_msg
