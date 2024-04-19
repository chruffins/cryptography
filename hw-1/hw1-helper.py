import math
from ciphers import Shift

def coprime(a, b):
    return math.gcd(a, b) == 1

def problem1():
    # A student wants to build an affine cipher for an alphabet with m = 1735. How many possible key choices do they have? Provide reasoning.
    print("problem 1:")
    # find all numbers coprime with 1735 to get number of a's
    num_a = 0
    for i in range(1, 1735): # can't include zero because it destroys information
        if coprime(i, 1735):
            num_a += 1

    # b can be 0-1734 inclusive so just times by 1735 lol
    print(f"there are {num_a * 1735} possible keys")
    print(f"because there are {num_a} choices for a")
    print("and 1735 choices for b.")

class Bitfield():
    def __init__(self, bits: list[int]) -> None:
        self.bits: list[int] = bits
    
    def __int__(self) -> int:
        l = len(self) - 1
        r = 0
        for i, b in enumerate(self.bits):
            r += 2**(l-i) * b
        return r

    def __len__(self) -> int:
        return len(self.bits)
    
    def __getitem__(self, key):
        return self.bits[key]
    
    def __setitem__(self, key, value):
        self.bits[key] = value
    
    def __repr__(self):
        return f"Bitfield({repr(self.bits)}, {int(self)})"
    
    def from_int(num: int):
        return Bitfield(list(map(int, bin(num)[2:])))
    
    def copy(self):
        return Bitfield(self.bits)

def problem4():
    # encrypt x and get y
    s_box: dict[int, int] = {
        0x0: 0xE,
        0x1: 0x4,
        0x2: 0xD,
        0x3: 0x1,
        0x4: 0x2,
        0x5: 0xF,
        0x6: 0xB,
        0x7: 0x8,
        0x8: 0x3,
        0x9: 0xA,
        0xA: 0x6,
        0xB: 0xC,
        0xC: 0x5,
        0xD: 0x9,
        0xE: 0x0,
        0xF: 0x7,
    }
    p_box: dict[int, int] = {
        1: 1,
        2: 5,
        3: 9,
        4: 13,
        5: 2,
        6: 6,
        7: 10,
        8: 14,
        9: 3,
        10: 7,
        11: 11,
        12: 15,
        13: 4,
        14: 8,
        15: 12,
        16: 16
    }
    
    k = [int(x, 2) for x in ['0011', '1010', '1001', '0100', '1101', '0110', '0011', '1111']]
    keys = []
    for i in range(5):
        keys.append((k[i] << 12) + (k[i+1] << 8) + (k[i+2] << 4) + (k[i+3]))

    x = Bitfield.from_int(0b1001110000011111)
    w0 = x.copy()
    k1 = Bitfield.from_int(keys[0])
    u1 = x ^ k1
    v1 = (s_box(u1 >> 12 & 0xF) << 12) + (s_box(u1 >> 8 & 0xF) << 8) + (s_box(u1 >> 4 & 0xF) << 4) + (s_box(u1 & 0xF))

if __name__ == "__main__":
    s = Shift(1, 5, 27)
    b = Bitfield.from_int(5)

    #problem1()
    #print(s.encode("helloworld"))
    #print(s.decode(s.encode("helloworld")))