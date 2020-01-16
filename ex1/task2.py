import matplotlib.pyplot as plt
import numpy as np 
from util import point, draw_frame

#Camera constants
fx = 1075.47
fy = 1077.22
cx = 621.01
cy = 362.80

#Camera matrix
K = np.array([
            [fx, 0, cx],
            [0, fy, cy],
            [0, 0, 1]])

#Projection matrix
PI = np.array([[1,0,0,0], [0,1,0,0], [0,0,1,0]])

#Platform-to-camera matrix
plat_to_cam = np.array([
                    [0.894372, -0.447712, 0.0127064, -0.25861],
                    [-0.0929288, -0.213413, -0.972924, 0.116584],
                    [0.438049, 0.868713, -0.232355, 0.791487],
                    [0, 0, 0, 1]])

s2s = 0.1145 #screw to screw distance, in m
#points given in platform coordinate frame, each corner of platform
platform_corners = np.array([[0,0,0,1], [s2s,0,0,1], [s2s,s2s,0,1], [0,s2s,0,1]])

#loading image
img = plt.imread("quanser.jpg")
plt.imshow(img)
h, w = img.shape[0:2]

#transforming platform points to camera
KPI = K@PI
platform_camera = plat_to_cam@platform_corners.T
scale_platform = 1/platform_camera[2,:]
x_platform = scale_platform * (KPI@platform_camera)
plt.scatter(x_platform[0,:], x_platform[1,:])

draw_frame(plat_to_cam, KPI)
plt.xlim([0,w])
plt.ylim([h,0])
plt.show() 