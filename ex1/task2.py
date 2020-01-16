import matplotlib.pyplot as plt
import numpy as np 
from util import *

### System parameters   ###
s2s = 0.1145                #screw to screw distance [m], for platform
d_base_hinge = 0.325        #distance from base to hinge [m]
d_hinge_arm = -0.0552       #distance from hinge to arm [m]
d_arm_carriage_x = 0.653    #distance from arm to rotor carriage along x [m]
d_arm_carriage_z = -0.0312  #distance from arm to rotor carriage along z [m]

psi = 11.77                 #angle from platform to base, around z
theta = 28.87               #angle from base to arm/hinge, around y
phi = -0.5                  #pitch angle, around x

### Camera constants    ###
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
T_plat_to_cam = np.array([
                    [0.894372, -0.447712, 0.0127064, -0.25861],
                    [-0.0929288, -0.213413, -0.972924, 0.116584],
                    [0.438049, 0.868713, -0.232355, 0.791487],
                    [0, 0, 0, 1]])

KPI = K@PI

### task2_a ###
#points given in platform coordinate frame, each corner of platform
platform_corners = np.array([[0,0,0,1], [s2s,0,0,1], [s2s,s2s,0,1], [0,s2s,0,1]])


### task2_b ###
#loading image
img = plt.imread("quanser.jpg")
plt.imshow(img)
h, w = img.shape[0:2]
plt.xlim([0,w])
plt.ylim([h,0])

#transforming platform points to camera
platform_camera = T_plat_to_cam@platform_corners.T
scale_platform = 1/platform_camera[2,:]
x_platform = scale_platform * (KPI@platform_camera)
plt.scatter(x_platform[0,:], x_platform[1,:])
#Drawing axis at platform origo
length_of_axis = 1/10   #Must scale length of axis, else it will be like 1000px long...
draw_frame(T_plat_to_cam, KPI, length_of_axis)
    
### task2_c ###
#Translating from platform to base, then rotate around z
T_base_to_plat = T_plat_to_cam@T_xyz(s2s/2, s2s/2, 0)@R_z(psi)
draw_frame(T_base_to_plat, KPI, length_of_axis)

### task_2_d ###
#Translating from base to hinge in z, then rotate around y
T_hinge_to_base = T_base_to_plat@T_xyz(0,0, d_base_hinge)@R_y(theta)
#Translating in z after rotation ^ to find arm 
T_arm_to_hinge = T_hinge_to_base@T_xyz(0,0, d_hinge_arm)
draw_frame(T_hinge_to_base, KPI, length_of_axis)
draw_frame(T_arm_to_hinge, KPI, length_of_axis)

### task_2_e ###
#translate x AND z, then rotate around x
T_rotors_to_arm = T_arm_to_hinge@T_xyz(d_arm_carriage_x, 0, d_arm_carriage_z)@R_x(phi)
draw_frame(T_rotors_to_arm, KPI, length_of_axis)

### task_2_f ###
fid_points = np.loadtxt("heli_points.txt")
#first 3 points in arm frame, last 4 points are in rotors frame
T_arm_frame = T_arm_to_hinge
arm_fids = T_arm_frame@fid_points[:3, :].T
arm_scale = 1/arm_fids[2,:] #1/Z
arm_fids = KPI@arm_fids * arm_scale
plt.scatter(arm_fids[0,:], arm_fids[1,:])

T_rotor_frame = T_rotors_to_arm
rotor_fids = T_rotor_frame@fid_points[3:, :].T
rotor_scale = 1/rotor_fids[2,:]
rotor_fids = KPI@rotor_fids * rotor_scale
plt.scatter(rotor_fids[0,:], rotor_fids[1,:])

plt.show() 