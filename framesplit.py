import cv2
import numpy
import time
import sys 
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import functions


#BALL_DIA = 7.1*(1.0/100) #meter
BALL_DIA = 10*(1.0/100) #meter
RADIUS_PIXEL = 111 #px

DISTANCE_PER_PIXEL = BALL_DIA/(2*(RADIUS_PIXEL))
print DISTANCE_PER_PIXEL

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
    if(count>5 and count<14):
        x,y = functions.process_frame(frame, filename='img'+str(count))
        #x,y = functions.process_frame(frame)
        if x and y:
            positions.append((x,y))
            frames.append(count)

print "POSITIONS **"
print positions
print "POSITIONS **"

#plt.plot([x[0] for x in positions], frames)
plt.subplot(3, 1, 1)
pos_modified = [ (p[0]*DISTANCE_PER_PIXEL, p[1]*DISTANCE_PER_PIXEL) for p in positions ]
plt.plot(frames, pos_modified)
#plt.show()
velocity = [(0,0),]
for i in range(1,len(positions)):
    xn, yn = positions[i]
    xo, yo = positions[i-1]
    #delta_time = frames[i] - frames[i-1]
    delta_time = 1.0/30
    #velocity.append(((xn-xo)*DISTANCE_PER_PIXEL/float(delta_time), (yn-yo)*DISTANCE_PER_PIXEL/float(delta_time)))
    vx = (xn-xo)*DISTANCE_PER_PIXEL/float(delta_time)
    vy = (yn-yo)*DISTANCE_PER_PIXEL/float(delta_time)
    print "vx,vy: ",vx,vy
    velocity.append((vx,vy))

plt.subplot(3, 1, 2)
plt.plot(frames[1:], velocity[1:])

acceleration = [(0,0),]
for i in range(2,len(velocity)):
    xn, yn = velocity[i]
    xo, yo = velocity[i-1]
    #delta_time = frames[i] - frames[i-1]
    delta_time = 1.0/30
    acceleration.append(((xn-xo)/float(delta_time), (yn-yo)/float(delta_time)))

plt.subplot(3, 1, 3)
plt.plot(frames[3:-1], acceleration[2:-1])
plt.show()
print count, "Count"
