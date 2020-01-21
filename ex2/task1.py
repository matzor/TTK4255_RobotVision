import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

fx = 9.842439e+02
cx = 6.900000e+02
fy = 9.808141e+02
cy = 2.331966e+02
k1 = -3.728755e-01
k2 = 2.037299e-01
p1 = 2.219027e-03
p2 = 1.383707e-03
k3 = -7.233722e-02

# Camera matrix
K = np.array([  [fx, 0, cx],
                [0, fy, cy],
                [0, 0, 1]])

K_inv = np.array([  [1/fx,  0,      -cx],
                    [0,     1/fy,   -cy],
                    [0,     0,       1]])

PI = np.array([[1,0,0,0], [0,1,0,0], [0,0,1,0]])

# Distortion
dist_coeffs = np.array([k1,k2,p1,p2,k3])

# Testing with OpenCV
img_src = plt.imread("data/kitti.jpg")
img_dst = cv.undistort(img_src, K, dist_coeffs, K_inv)
plt.imshow(img_dst)
plt.savefig("data/opencv_undistort.png")
plt.show()
