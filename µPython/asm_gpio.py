from machine import Pin

led = Pin("D13")


@micropython.asm_thumb
def fast_blink(r0):
    mov(r1, 2)
    # move a big value into r2, say 1<<20
    data(2, 0b11110_1_0_0010_0_1111, 0b0_001_0010_10000000)
    label(start)
    str(r1, [r0, 0])
    sub(r2, r2, 1)
    cmp(r2, 0)
    bgt(start)


BASE = 0x41008000 + 0x80 + 0x1C
fast_blink(BASE)
