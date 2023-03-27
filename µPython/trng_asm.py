from machine import mem32
from array import array
from uctypes import addressof

counts = array("I", [0 for j in range(32)])

# inputs
# r0: pointer to counts
# r1: pointer to TRNG data register
# r2: number of iterations

# working
# r3: scratch register 0...31
# r4: scratch register for random number
# r5: scratch register for accumulate
# r6: scratch register for add
# r7: working register for ldr / str


# test & with r0 & #1
@micropython.asm_thumb
def trng_test(r0, r1, r2):
    push({r4, r5, r6, r7})

    label(start)
    ldr(r4, [r1, 0])
    mov(r3, 32)
    mov(r7, r0)
    label(accumulate)
    ldr(r6, [r7, 0])
    data(2, 0xF004, 0x0501)
    add(r6, r6, r5)
    str(r6, [r7, 0])
    add(r7, r7, 4)
    data(2, 0x0864)
    sub(r3, r3, 1)
    cmp(r3, 0)
    bne(accumulate)
    sub(r2, r2, 1)
    cmp(r2, 0)
    bne(start)

    pop({r4, r5, r6, r7})


# set up TRNG

# MCLK enable -> BASE = 0x40000800 (p51)
# BASE + 0x1C (APBCMASK) -> bit 10 needs to be toggled (read / modify / write or xor?)

MCLK_BASE = 0x40000800
APBCMASK = MCLK_BASE | 0x1C

mem32[APBCMASK] = mem32[APBCMASK] | 1 << 10

# TRNG -> BASE = 0x42002800
# TRNG enable -> BASE -> bit 1 needs to be toggled

TRNG_BASE = 0x42002800
mem32[0x42002800] = mem32[0x42002800] | 1 << 1

# read from RNG -> assuming that this is _so slow_ that I don't need to wait for
# the interrupt to tell me it is ready

TRNG_DATA = TRNG_BASE | 0x20

N = 1000

trng_test(addressof(counts), TRNG_DATA, 2 * N * N)

for j in range(32):
    print(f"{j:02x} {(counts[j] - N * N) / N:.3f}")
