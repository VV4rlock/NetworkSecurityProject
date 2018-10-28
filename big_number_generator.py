import random
import math
from gmpy2 import mpz, isqrt, invert, powmod,jacobi
from gmpy2 import random_state, mpz_urandomb


class CryptoObject():
    def __init__(self):
        self.random_state=random_state()

    @staticmethod
    def jacobi(a, n): #???????????
        if a == 1: return 1
        if a == 0: return 0
        if a < 0:
            return -CryptoObject.jacobi(-a, n) if n & 2 else CryptoObject.jacobi(-a, n)
        e = 0
        while a & 1 == 0:
            a >>= 1
            e += 1
        if e & 1 == 0 or n & 7 == 1 or n & 7 == 7:
            s = 1
        else:
            s = -1
        if n & 3 == 3 and a & 3 == 3:
            s = -s
        if a == 1:
            return s
        return s*CryptoObject.jacobi(n % a, a)

    @staticmethod
    def is_prime(n, k=4):
        if not n & 1:
            return False
        var = []
        for _ in range(k):
            a = random.randint(1, n-1)
            while a in var:
                a = random.randint(1, n-1)
            var.append(a)
            if math.gcd(a, n) != 1:
                return False
            r = powmod(a, (n - 1) // 2, n)
            if r != 1 and r != n-1:
                return False
            s=jacobi(a, n)
            if s < 0:
                s += n
            if r != s:
                return False
        return True


    def gen_big_random(self, l=0, r=1024):
        """ generates a large random number m: 2**l <= m < 2**r """
        assert l < r, 'Lower border of the range should be strictly less than the upper one!'
        lv, rv = mpz(1) << l, mpz(1) << r
        lh = mpz_urandomb(self.random_state, l)
        rh = mpz_urandomb(self.random_state, r - l) << l
        b = (lh + lv + rh) % rv
        return b

    def gen_big_prime(self,key_length=1024):
        out = self.gen_big_random(key_length - 1, key_length)
        while True:
            out += 2
            if CryptoObject.is_prime(out, key_length):
                return out


    @staticmethod
    def str_to_int(s):
        return mpz(s, 16)

    @staticmethod
    def int_to_str(i):
        return i.digits(16)

    def get_random_bytes(self, length):
        '''lenght - count of random bytes'''
        out=self.gen_big_random(length*8-1, length*8)
        return out#self.int_to_str(out)


if __name__=="__main__":
    #a,b,c=3,188888882,10111113544441
    crypto_object=CryptoObject()
    print(crypto_object.get_random_bytes(15))



