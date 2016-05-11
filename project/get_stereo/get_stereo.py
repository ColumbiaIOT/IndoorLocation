import RPi.GPIO as gp
import os
import time
import sys

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

def main():

    timestamp = int(time.time())
    """
    LEFT CAMERA <- Camera A
    """
    gp.output(7, False)
    gp.output(11, False)
    gp.output(12, True)
    capture('L', sys.argv[1])
    """
    RIGHT CAMERA <- Camera C
    """
    gp.output(7, False)
    gp.output(11, True)
    gp.output(12, False)
    capture('R', sys.argv[1])

def capture(cam, timestamp):

    cmd = "raspistill -n -o %s_%s.jpg" % (timestamp, cam)
    os.system(cmd)

if __name__ == '__main__':

    main()
