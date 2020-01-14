import matplotlib.pyplot as plt
import numpy as np 

box = np.loadtxt('box.txt')

#Camera constants:
f_x = 1000
f_y = 1100 
c_x = 320 
c_y = 240

#Camera matrix
K = np.array([[f_x, 0, c_x],
            [0, f_y, c_y],
            [0, 0, 1]])

PI = np.array([[1,0,0,0], [0,1,0,0], [0,0,1,0]])

tz = 6
theta = 30

#points
def u(X,Z):
    return c_x + f_x * X/Z

def v(Y,Z):
    return c_y + f_y * Y/Z

#rotation matrices
def T_z(tz):
    Tz = np.identity(4)
    Tz[2, 3] = tz
    return Tz

def R_x(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[1, 0, 0, 0],
                    [0, c, -s, 0],
                    [0, s, c, 0],
                    [0, 0, 0, 1]])

def R_y(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, 0, s, 0],
                    [0, 1, 0, 0],
                    [-s, 0, c, 0],
                    [0, 0, 0, 1]])

def R_z(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s, 0, 0],
                    [s, c, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])

#plot help functions
def draw_line(a, b, label="", **args):
    ax = u(a[0, 0], a[2, 0])
    ay = v(a[1, 0], a[2, 0])
    bx = u(b[0, 0], b[2, 0])
    by = v(b[1, 0], b[2, 0])

    plt.plot([ax, bx], [ay, by], **args)

#Old, buggy version... 1b)
""" #initialize image coordiante vector x
x = np.zeros([len(box), 3])
x[:,2] = 1

#Transforming points from world to camera
for i in range(len(box)):
    x[i,:] = K@PI@T_z(tz)@box[i,:] #K@PI@T_z(tz)@R_x(theta)@R_y(theta)@box[i,:]

plt.figure()
plt.scatter(x[:,0], x[:,1]) 
plt.show() """

#Task 1b:
box_camera = T_z(6)@box.T
x = K@PI@box_camera
scaleing_factor = 1/box_camera[2,:]
x = scaleing_factor * x

plt.figure()
#plt.subplot(121)
plt.scatter(x[0,:], x[1,:])
plt.grid()
plt.xlim([0,640])
plt.ylim([480,0])


"""#Task 1d
x2 = K@PI@R_x(theta)@R_y(theta)@box.T
plt.subplot(121)
plt.scatter(x2[0,:], x2[1,:])
plt.grid()
plt.xlim([0,640])
plt.ylim([480,0])"""

plt.show() 