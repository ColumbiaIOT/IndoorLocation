import timeit

setup = """\
import RPi.GPIO as gp
import picamera

gp.setwarnings(False)
gp.setmode(gp.BOARD)

gp.setup(7,  gp.OUT)
gp.setup(11, gp.OUT)
gp.setup(12, gp.OUT)
gp.setup(15, gp.OUT)
gp.setup(16, gp.OUT)
gp.setup(21, gp.OUT)
gp.setup(22, gp.OUT)

gp.output(11, True)
gp.output(12, True)
gp.output(15, True)
gp.output(16, True)
gp.output(21, True)
gp.output(22, True)

def switch():

    gp.output(7, False)
    gp.output(11, True)
    gp.output(12, False)
    
gp.output(7, False)
gp.output(11, False)
gp.output(12, True)
"""
print timeit.timeit('switch()', setup=setup, number=1000)
