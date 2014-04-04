import cv2
import numpy
import time
import sys 
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import functions



# Main execution starts here
#plt.show()
cap = cv2.VideoCapture("/home/anhad/Videos/sc2_3.mp4");
print cap.isOpened()

count=0
positions = []
frames = []
while True:
    ref, frame = cap.read()
    if frame is None:
        break
    #print type(frame), frame.shape
    count+=1
    #x,y = functions.process_frame(frame, filename='img'+str(count))
    x,y = functions.process_frame(frame)
    if x and y:
        positions.append((x,y))
        frames.append(count)

#plt.plot([x[0] for x in positions], frames)
plt.subplot(3, 1, 1)
plt.plot(frames, positions)
#plt.show()
velocity = [(0,0),]
for i in range(1,len(positions)):
    xn, yn = positions[i]
    xo, yo = positions[i-1]
    delta_time = frames[i] - frames[i-1]
    velocity.append(((xn-xo)/float(delta_time), (yn-yo)/float(delta_time)))

plt.subplot(3, 1, 2)
plt.plot(frames, velocity)

acceleration = [(0,0),]
for i in range(1,len(velocity)):
    xn, yn = velocity[i]
    xo, yo = velocity[i-1]
    delta_time = frames[i] - frames[i-1]
    acceleration.append(((xn-xo)/float(delta_time), (yn-yo)/float(delta_time)))

plt.subplot(3, 1, 3)
plt.plot(frames, acceleration)
plt.show()
print count, "Count"
