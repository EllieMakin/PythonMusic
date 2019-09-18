from __future__ import division
from SongBasic import *
import os
import random

volume = 100
rate = random.gauss(5, 5) 
base = 12
gap = 2**(1/base)   
transpose = 0
length = 500
tracks = int(random.uniform(1, 5))

chars = "*/[{"
styles = [["M", "m"], ["d", "p", "a"]]
final = [rate]

for track in range(tracks):
    test = [str(random.uniform(100, 1000))]
    for i in range(length):
        choice = int(random.uniform(0, 4))
        test.append(chars[choice])
        if choice == 2:
            test.append(str(int(random.gauss(0, 4))))
            test.append("]")
        elif choice == 3:
            chrd = ["#"]
            chrd.append(random.choice(styles[0]))
            chrd.append(random.choice(styles[1]))
            test.append("".join(chrd))
            test.append("}")
    final.append("".join(test))

name = "random"
song(name, volume, base, gap, transpose, final)
command = "start C:\Users\eliot\Documents\Test\Python\Sound\Sound.pyproj\\" + name + ".wav"

os.system(command)
