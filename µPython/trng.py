from machine import mem32

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

counts = {}
for j in range(32):
    counts[j] = 0

for j in range(200):
    a = mem32[TRNG_DATA]
    for k in range(32):
        counts[k] += (a & 1 << k) >> k

for j in range(32):
    print(f"{j:02d} {0.1 * (counts[j] - 100):.1f}")
