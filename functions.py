import cv2
import numpy
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def smoothing_kernel2D(n):
    kernel = numpy.ndarray((n,n), float)
    kernel[:,:] = 1.0/n**2

    return kernel

def COM(mylist):
    return reduce( lambda o,n: (o[0]+n[0], o[1]+n[0]*n[1]), enumerate(mylist), (0,0))

def FindCenter(img):
    """ Takes a 2D array (dimensionality of 2)"""

    xmass, ymass, totalmass = 0, 0, 0
    for y,l in enumerate(img):
        for x,wt in enumerate(l):
            if wt==255:
                xmass+=x*1
                ymass+=y*1
                totalmass+=1
            
    if totalmass == 0:
        return None, None
    return xmass*1.0/totalmass, ymass*1.0/totalmass


def process_frame(frame, filename=None):
    ##frame[:,:,2]=0
    ##frame[:,:,1]=0
    ##frame[:,:,0]=0
    ##print frame
    orig_frame = numpy.copy(frame)
    new_frame = frame[:,:,2]
    
    new_new_frame = cv2.filter2D(new_frame, -1, smoothing_kernel2D(25))
    
    # Histogram
    #hist = cv2.calcHist([new_new_frame], [0], None, 256, [0,256])
    #plt.hist(new_new_frame.ravel(), 256, [0,256]);
    #plt.show()
    
    print "NEW_FRAME", type(new_new_frame)
    print "Max, new_new_frame", numpy.amax(new_new_frame)
    thresholding_filter = numpy.vectorize(lambda x: 255 if x>30 else 0)
    filtered_frame = thresholding_filter(new_new_frame)
    
    print "max, filtered", numpy.amax(filtered_frame)
    print filtered_frame


    #Mark center of frame
    cx, cy = FindCenter(filtered_frame)
    if cx and cy:
        filtered_frame[int(cy)-5:int(cy)+5, int(cx)-5:int(cx)+5] = 128

    #marked_frame = 
    mask = numpy.ndarray(filtered_frame.shape, dtype=int)
    mask[:,:] = 255
    print "MASK:", mask
    
    inverted_filter = numpy.bitwise_xor(mask, filtered_frame)
    frame_ball_marked = numpy.bitwise_and(orig_frame, numpy.dstack([inverted_filter]*3))
    
    # Show grey scale
    if filename:
        plt.imshow(filtered_frame, cmap=cm.Greys_r)
        plt.savefig(filename+".png", format='png')
        plt.clf()
        plt.imshow(frame_ball_marked)
        #plt.imshow(frame)
        plt.savefig(filename+"Marked.png", format='png')
    else:
        #plt.show()
        pass

    return cx, cy
