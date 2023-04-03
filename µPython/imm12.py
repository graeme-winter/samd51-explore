import sys


def fmt(values):
    assert len(values) == 12
    null = ""
    return f"{values[0]}_{null.join(values[1:4])}_{null.join(values[4:])}"


if "x" in sys.argv[1]:
    a = int(sys.argv[1], 16)
else:
    a = int(sys.argv[1])

if a < 0x100:
    print(fmt(format(a, "012b")))
    sys.exit(0)

stra = format(a, "032b")

if stra.rindex("1") - stra.index("1") > 7:
    sys.exit("cannot decode without information loss")

s = stra.index("1") + 8
r = stra[s:] + stra[:s]

word = format(s, "05b") + r[-7:]
print(fmt(format(s, "05b") + r[-7:]))
