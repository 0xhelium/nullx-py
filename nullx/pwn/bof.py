import math
import string
import random

class StackOffsetCalculator:
    class OutOfDigitsError(Exception):
        pass

    '''
    def _get_group(self, i, slots=2):
        gsize = math.floor(256 / slots)
        s = i * gsize
        e = (i + 1) * gsize - 1
        return s, e + 1

    def _increment_counter(self, c):
        for ci in range(len(c) - 1, -1, -1):
            cv = c[ci]
            gstart, gend = self._get_group(ci, slots=len(c))
            if (c[ci] + 1) < gend:
                c[ci] += 1
                return
            else:
                c[ci] = 0
        raise StackOffsetCalculator.OutOfDigitsError("Out of digits")

    def gen(self, length=200):
        c = [0] * 2
        u = bytes()
        for i in range(int(length / 2)):
            u += bytes(c)
            self._increment_counter(c)
        return u
    '''

    DIGITS = [string.ascii_uppercase, string.ascii_lowercase, string.digits]
    def _increment_characters(self, c):
        for ci in range(len(c) - 1, -1, -1):
            i = self.DIGITS[ci].index(c[ci])
            if (i + 1) < len(self.DIGITS[ci]):
                c[ci] = self.DIGITS[ci][i + 1]
                return
            else:
                c[ci] = self.DIGITS[ci][0]
        raise StackOffsetCalculator.OutOfDigitsError("Out of digits")

    def gen(self, length=1000):
        c = [d[0] for d in self.DIGITS]
        u = bytes()
        for i in range(int(length / 3)):
            u += bytes("".join(c).encode("utf-8"))
            self._increment_characters(c)
        return u
    
    def calc(self, target, length=200):
        return self.gen(length=length).index(target)
