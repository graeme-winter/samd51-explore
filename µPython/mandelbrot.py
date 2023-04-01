@micropython.asm_thumb
def mandel_asm(r0, r1):
    push({r4, r5, r6, r7, r8, r9})

    # save Ci, Cr to working registers
    mov(r2, r1)
    mov(r1, r0)

    # initialise iter, Zr, Zi
    mov(r0, 0)
    mov(r3, 0)
    mov(r4, 0)

    label(iter)

    # compute squares -> z8, z9
    # Zr^2 -> SMULL r3, r3 -> r6, r7 §4.6.150
    data(2, 0b11111_0111_0_00_0011, 0b0110_0111_0000_0011)
    # now right shift LO by 24
    lsr(r6, r6, 24)
    # shift left everything else by 8 & orr §4.6.92
    data(2, 0b11101_01_0010_0_0110, 0b0_010_1000_00_00_0111)
    # Zi^2 -> SMULL r4, r4 -> r6, r7 §4.1.87
    data(2, 0b11111_0111_0_00_0100, 0b0110_0111_0000_0100)
    # now right shift LO by 24
    lsr(r6, r6, 24)
    # shift left everything else by 8 & orr §4.6.92
    data(2, 0b11101_01_0010_0_0110, 0b0_010_1001_00_00_0111)

    # Add r8, r9 -> r5 §4.6.4 encoding T3 to reach high registers
    data(2, 0b11101_01_1000_0_1000, 0b0_000_0101_00_00_1001)

    # cmp because big value; §4.6.29
    data(2, 0b11110_0_0_1101_1_0101, 0b0_110_1111_10000000)
    bge(end)

    # next zr - SUB encoding at §4.6.177 to reach high registers
    mov(r5, r3)
    data(2, 0b11101_01_1101_0_1000, 0b0_0000_0110_00_00_1001)
    add(r3, r6, r1)

    # next zi - SMULL etc.
    data(2, 0b11111_0111_0_00_0101, 0b0110_0111_0000_0100)
    lsr(r6, r6, 24)
    data(2, 0b11101_01_0010_0_0110, 0b0_010_0101_00_00_0111)
    data(2, 0b11101_01_1000_0_0010, 0b0_000_0100_01_00_0101)

    add(r0, 1)
    # cmp because big value; §4.6.29
    data(2, 0b11110_1_0_1101_1_0000, 0b0_101_1111_10000000)
    bne(iter)

    label(end)

    pop({r4, r5, r6, r7, r8, r9})
