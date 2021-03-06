import matplotlib.pyplot as plt
import numpy as np
from common import draw_frame

def estimate_H(xy, XY):
    #
    # Task 2: Implement estimate_H
    #
    H_size = [3, 3]
    A = np.empty([0, 9])
    for row in range(XY.shape[0]):
        X = XY[row, 0]
        Y = XY[row, 1]
        x = xy[row, 0]
        y = xy[row, 1]

        row1 = np.array([X, Y, 1, 0, 0, 0, -X*x, -Y*x, -x])
        row2 = np.array([0, 0, 0, X, Y, 1, -X*y, -Y*y, -y])
        
        A = np.vstack([A, row1])
        A = np.vstack([A, row2])

    #Solve A@h = 0 by SVD
    _, _, V = np.linalg.svd(A, full_matrices=True, compute_uv=True)
    V = V.T
    #Only want last column of V.T, which is the arg min
    h = V[:, -1]
    H = np.reshape(h, H_size)
    return H

def decompose_H(H):
    #
    # Task 3a: Implement decompose_H
    #
    t  = H[:, 2]
    r1 = H[:, 0]
    r2 = H[:, 1]
    
    scale = np.linalg.norm(r2)
    r1 = (1/scale) * r1
    r2 = (1/scale) * r2
    t  = (1/scale) * t
    r3 = np.cross(r1, r2)

    T1 = np.column_stack((r1, r2, r3, t))
    T1 = np.vstack([T1, [0, 0, 0, 1]])
    T2 = -1*T1
    return T1, T2

def choose_solution(T1, T2):
    #
    # Task 3b: Implement choose_solution
    #
    #Check if z-translation is positive
    if T1[2, 3] > 0: 
        T = T1
    else:
        T = T2
    return T

K           = np.loadtxt('../data/cameraK.txt')
all_markers = np.loadtxt('../data/markers.txt')
XY          = np.loadtxt('../data/model.txt')
n           = len(XY)

for image_number in range(23):
    I = plt.imread('../data/video%04d.jpg' % image_number)
    markers = all_markers[image_number,:]
    markers = np.reshape(markers, [n, 3])
    matched = markers[:,0].astype(bool) # First column is 1 if marker was detected
    uv = markers[matched, 1:3] # Get markers for which matched = 1

    # Convert pixel coordinates to normalized image coordinates
    xy = (uv - K[0:2,2])/np.array([K[0,0], K[1,1]])

    H = estimate_H(xy, XY[matched, :2])
    T1,T2 = decompose_H(H)
    T = choose_solution(T1, T2)

    # Compute predicted corner locations using model and homography
    uv_hat = (K@H@XY.T)
    uv_hat = (uv_hat/uv_hat[2,:]).T

    plt.clf()
    plt.imshow(I, interpolation='bilinear')
    draw_frame(K, T, scale=7)
    plt.scatter(uv[:,0], uv[:,1], color='red', label='Observed')
    plt.scatter(uv_hat[:,0], uv_hat[:,1], marker='+', color='yellow', label='Predicted')
    plt.legend()
    plt.xlim([0, I.shape[1]])
    plt.ylim([I.shape[0], 0])
    plt.savefig('../data/out%04d.png' % image_number)
