import matplotlib.pyplot as pyplot
import matplotlib.image as mpimg
import numpy as np

img = pyplot.imread("roomba.jpg")
h, w = img.shape[0:2]
print("Height: %d, width: %d" %(h, w))
#img = img[:,:,2]    #r,g,b = 0, 1, 2 
rimg = img
rimg = rimg/255.0

difference = rimg - np.array([1.0, 0.0, 0.0])
distance = np.linalg.norm(difference, axis=2)
threshold = distance < 0.6

pyplot.imshow(rimg[:,:,0] > threshold)

pyplot.show()