import matplotlib.pyplot as plt 
import numpy as np 

img = plt.imread("roomba.jpg")
h, w = img.shape[0:2]

print("image height: %d, image width: %d" %(h, w))

plt.subplot('131')
plt.title("Original image")
plt.imshow(img)

plt.subplot('132')
plt.title("Naive threshold")
threshold = 0.4
img = img/255.0
plt.imshow(img[:,:,0] > threshold)

plt.subplot('133')
plt.title("Color distance")
color_ref = np.array([1.0, 0.0, 0.0])
difference = img - color_ref
distance = np.linalg.norm(difference, axis=2)
threshold = distance > 0.6
plt.imshow(img[:,:,0] > threshold)


plt.savefig("img_result.png")
plt.show()