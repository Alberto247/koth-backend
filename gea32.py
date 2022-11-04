import random


def nl(x0, x1, x2, x3, x4, x5, x6):
    res = x0*x2*x5*x6 + x0*x3*x5*x6 + x0*x1*x5*x6 + x1*x2*x5*x6 + x0*x2*x3*x6 + x1*x3*x4*x6 + x1*x3*x5*x6 + x0*x2*x4 + x0*x2*x3 + x0*x1*x3 + x0*x2*x6 + x0*x1*x4 + x0*x1*x6 + x1*x2*x6 + x2*x5*x6 + x0*x3*x5 + x1*x4*x6 + x1*x2*x5 + x0*x3 + x0*x5 + x1*x3 + x1*x5 + x1*x6 + x0*x2 + x1 + x2*x3 + x2*x5 + x2*x6 + x4*x5 + x5*x6 + x2 + x3 + x5
    return res % 2


class LFSR:
    def __init__(self, n, bits, taps, out_idx):
        self.state = [0]*n
        self.taps = taps
        self.out_idx = out_idx

        for b in bits:
            self._clock(b)

    def _clock(self, inp=0):
        out = self.state[0] ^ inp
        self.state = self.state[1:] + [0]
        for i in self.taps:
            self.state[i] ^= out

    def get_bits(self, n):
        res = 0
        for _ in range(n):
            res <<= 1
            out_bits = [self.state[idx] for idx in self.out_idx]
            res += self.state[0]
            #res += nl(*out_bits)
            self._clock()
        return res


class GEA:
    def __init__(self, state, taps, shifts, out_idxs, ns):
        self.lfsr = [LFSR(n, state[s:]+state[:s], t, oi) for s, t, oi, n in zip(shifts, taps, out_idxs, ns)]

    def get_bits(self, n):
        res = 0
        for lfsr in self.lfsr:
            res ^= lfsr.get_bits(n)
        return res

    def randint(self, min, max):
        range=max-min+1
        assert range>=0, "randint min>max"
        rnd = self.get_bits(1<<(range-1).bit_length().bit_length())
        rnd = (rnd % range) + min
        return rnd

