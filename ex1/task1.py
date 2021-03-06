import matplotlib.pyplot as plt
import numpy as np 

box = np.loadtxt('box.txt')

#Camera constants:
f_x = 1000
f_y = 1100 
c_x = 320 
c_y = 240

tz = 6
theta = 30

#Camera matrix
K = np.array([[f_x, 0, c_x],
            [0, f_y, c_y],
            [0, 0, 1]])

PI = np.array([[1,0,0,0], [0,1,0,0], [0,0,1,0]])

#points
def point(x, y, z):
    return np.array([[x], [y], [z], [1]])

#rotation matrices
def T_z(tz):
    Tz = np.identity(4)
    Tz[2, 3] = tz
    return Tz

def R_x(theta):
    rad = np.deg2rad(theta)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([[1, 0, 0, 0],
                    [0, c, -s, 0],
                    [0, s, c, 0],
                    [0, 0, 0, 1]])

def R_y(theta):
    rad = np.deg2rad(theta)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([[c, 0, s, 0],
                    [0, 1, 0, 0],
                    [-s, 0, c, 0],
                    [0, 0, 0, 1]])

def R_z(theta):
    rad = np.deg2rad(theta)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([[c, -s, 0, 0],
                    [s, c, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])

def draw_line(a, b, **args):
    plt.plot([a[0], b[0]], [a[1], b[1]], **args)

def draw_frame(T):
    origo = T@point(0,0,0)
    scale_o = 1/origo[2,:]
    origin = K@PI@origo
    origin = scale_o * origin
    axis = np.array([[1,0,0,1],[0,1,0,1],[0,0,1,1]])
    axis = T@axis.T
    scale_axis = 1/axis[2,:]
    X = K@PI@axis
    X = scale_axis * X
    x = X[:,0]
    y = X[:,1]
    z = X[:,2]
    draw_line(origin, x, color='r')
    plt.text(x[0],x[1], "X", color='r')
    draw_line(origin, y, color='g')
    plt.text(y[0],y[1], "Y", color='g')
    draw_line(origin, z, color='b')
    plt.text(z[0],z[1], "Z", color='b')

#Task 1b:
box_camera = T_z(tz)@box.T
x = K@PI@box_camera
scaling_factor = 1/box_camera[2,:] #1/Z
x = scaling_factor * x

plt.figure()
plt.subplot(121)
plt.scatter(x[0,:], x[1,:])
plt.grid()
plt.xlim([0,640])
plt.ylim([480,0])
plt.title("Original box")


#Task 1d
# Translate and rotate box
T_matrix = T_z(tz)@R_x(theta)@R_y(theta) #rotate y, rotate x, translate z
box_camera = T_matrix@box.T
x2 = K@PI@box_camera
scaling_factor = 1/box_camera[2,:] #1/Z
x2 = scaling_factor * x2
plt.subplot(122)
plt.scatter(x2[0,:], x2[1,:])
plt.grid()
plt.xlim([0,640])
plt.ylim([480,0])
plt.title("Rotated box")

#Plotting coordinate axis in box frame
draw_frame(T_matrix)

plt.show() 