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
plt.figure()
img_dst = cv.undistort(img_src, K, dist_coeffs)
plt.imshow(img_dst)
plt.title("OpenCV undistort")
plt.savefig("data/opencv_undistort.png")

### implementation

def get_distortion(x, y, dist_coeffs):
    #eq (5) and (6), distortion
    k1 = dist_coeffs[0] ; k2 = dist_coeffs[1]
    p1 = dist_coeffs[2] ; p2 = dist_coeffs[3]
    k3 = dist_coeffs[4]
    r = np.sqrt(x**2 + y**2)
    dist_rad = k1*r**2 + k2*r**4 + k3*r**6
    dist_tan_x = 2*p1*x*y + p2*(r**2 + 2*x**2)
    dist_tan_y = p1*(r**2 + 2*y**2) + 2*p2*x*y
    dx = dist_rad*x + dist_tan_x
    dy = dist_rad*y + dist_tan_y
    return dx, dy

def dst_x_y(u_dst, v_dst, camera_mtx):
    #inverting eq (1) and (2)
    fx = camera_mtx[0,0]; fy = camera_mtx[1,1]
    cx = camera_mtx[0,2]; cy = camera_mtx[1,2]
    x = 1/fx * (u_dst - cx)
    y = 1/fy * (v_dst - cy)
    return x, y

def src_u_v(x, y, camera_mtx, dx, dy):
    fx = camera_mtx[0,0]; fy = camera_mtx[1,1]
    cx = camera_mtx[0,2]; cy = camera_mtx[1,2]
    u_src = cx + fx*(x + dx)
    v_src = cy + fy*(y + dy)
    return int(round(u_src)), int(round(v_src))

#img_src_shape = img_src.shape
img_dst = np.zeros([img_src.shape[0], img_src.shape[1], img_src.shape[2]], dtype='uint8')

for row in range(0, img_src.shape[0]):
    for col in range(0, img_src.shape[1]):
        x, y = dst_x_y(col, row, K)
        dx, dy = get_distortion(x, y, dist_coeffs)
        u_src, v_src = src_u_v(x, y, K, dx, dy)

        if (v_src < img_src.shape[0]) and (u_src < img_src.shape[1]):
            img_dst[row, col, :] = img_src[v_src, u_src, :]

plt.figure()
plt.subplot(2,1,1)
plt.title("Original, distorted image")
plt.imshow(img_src)

plt.subplot(2,1,2)
plt.title("Undistorted image")
plt.imshow(img_dst)

plt.savefig("data/undistort.png")
plt.show()

