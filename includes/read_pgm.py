import re
import numpy as np
import os

#I have copied this function from http://stackoverflow.com/questions/7368739/numpy-and-16-bit-pgm
def read_pgm(filename, byteorder='>',transpose=False,invert_x=False,invert_y=False):
    """Return image data from a raw PGM file as numpy array. Format specification: http://netpbm.sourceforge.net/doc/pgm.html
        Note: transpose is executed BEFORE the x or y axis are inverted!"""
    with open(filename, 'rb') as f:
        buffer = f.read()
    try:
        header, width, height, maxval = re.search(
                                                  b"(^P5\s(?:\s*#.*[\r\n])*"
                                                  b"(\d+)\s(?:\s*#.*[\r\n])*"
                                                  b"(\d+)\s(?:\s*#.*[\r\n])*"
                                                  b"(\d+)\s(?:\s*#.*[\r\n]\s)*)", buffer).groups()
    except AttributeError:
        raise ValueError("Not a raw PGM file: '%s'" % filename)
    image=np.frombuffer(buffer, dtype='u1' if int(maxval) < 256 else byteorder+'u2', count=int(width)*int(height), offset=len(header)).reshape((int(height), int(width)))
    if transpose: image=image.T
    if invert_x: image=image[::-1,:]
    if invert_y: image=image[:,::-1]
    return image

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    imagepath="example_data/Mode7_Raw16.pgm"
    image = read_pgm(imagepath, byteorder='>')
    print(image)
    print(image.dtype)
    print('original image: min: %g, max: %g'%(np.min(image),np.max(image)))
    plt.imshow(image, plt.cm.gray)
    
    x,y=np.arange(image.shape[0]),np.arange(image.shape[1])
    X,Y=np.meshgrid(x,y)
    plt.figure()
    plt.pcolormesh(X,Y,image.T,cmap=plt.cm.gray)
    
    plt.show()