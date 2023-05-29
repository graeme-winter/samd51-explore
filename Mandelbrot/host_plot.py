import sys

import numpy
from matplotlib import pyplot
from PIL import Image

import serial

tty = serial.Serial(sys.argv[1])

NX = 1280
NY = 1280
NN = NX * 4


# save to allow file comparison
with open("out.dat", "wb") as f:
    for j in range(NY):
        block = tty.read(NN)
        f.write(block)

x = numpy.fromfile("out.dat", dtype=numpy.uint32, count=(NX * NY))
m = x.reshape((NY, NX))
m[m == 0x1000] = 0
m += 1

m = numpy.log2(m) * 18

image = m.astype(numpy.uint8)
Image.fromarray(image).save("mandel.png")
