# oh fuck
import numpy as np

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

q5_sbox = {
    0x0: 0x8, 0x1: 0x4, 0x2: 0x2, 0x3: 0x1,
    0x4: 0xC, 0x5: 0x6, 0x6: 0x3, 0x7: 0xD,
    0x8: 0xA, 0x9: 0x5, 0xA: 0xE, 0xB: 0x7,
    0xC: 0xF, 0xD: 0xB, 0xE: 0x9, 0xF: 0x0
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

s_box_inv = dict([(value, key) for key, value in s_box.items()])

def get_lin_approx_table(s_box: dict[int, int]):
    lin_approx = np.zeros((16, 16), dtype=np.uint8)
    for a in range(16):
        for b in range(16):
            for x in range(16):
                if (((a & x) ^ (b & s_box[x]))).bit_count() % 2 == 0:
                    lin_approx[a, b] += 1
    
    return lin_approx

def linear_attack(pairs: list[tuple[int, int]], s_box_inv: dict[int, int]):
    counts = np.zeros((16, 16), dtype=np.float64)

    #for a in range(16):
        #for b in range(16):
            #lin_approx[a,b] = 0
    for x, y in pairs:
        for a in range(16):
            for b in range(16):
                v_42 = a ^ ((y >> 8) & 0xF) # v4's 2nd 4 bit block
                v_44 = b ^ (y & 0xF) # v4's 4th 4 bit block
                u_42 = s_box_inv[v_42]
                u_44 = s_box_inv[v_44]
                # ugly but this is x_5, x_7, x_8, u4_6, u4_8, u4_14, u4_16 xor'd together
                z = (x >> 11 & 1) ^ (x >> 9 & 1) ^ (x >> 8 & 1) ^ (u_42 >> 2 & 1) ^ (u_42 & 1) ^ (u_44 >> 2 & 1) ^ (u_44 & 1)
                if z == 0: # requires even number of 1s
                    counts[a, b] += 1

    maxie = -1
    maxkey = None
    for a in range(16):
        for b in range(16):
            counts[a, b] = abs(counts[a, b] - (len(pairs) / 2))

            if counts[a, b] > maxie:
                maxie = counts[a, b]
                maxkey = (a,b)
    return maxkey

def import_data(fname: str) -> list[tuple[str,str]]:
    data = list()

    lines = open(fname, 'r').readlines()
    for line in lines:
        line = line.replace(' ', '').replace('\n', '')
        data.append((int(line[:16], 2), int(line[16:], 2)))
    
    return data

if __name__ == "__main__":
    lin_approx_table = get_lin_approx_table(q5_sbox)
    print("linear approximation table: ")
    print(lin_approx_table)
    #print(lin_approx_table)
    #data = import_data("KPAData.txt")
    #print(f"key blocks are {linear_attack(data, s_box_inv)}")