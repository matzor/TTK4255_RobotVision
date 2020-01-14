import matplotlib.pyplot as plt
import numpy as np 

box = np.loadtxt('box.txt')

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


def point(x,y,z):
    return np.array([[x], [y], [z], [1]])

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

#initialize image coordiante vector x
x = np.zeros([len(box), 3])
x[:,2] = 1

tz = 5
theta = 30

#Transforming points from world to camera
for i in range(len(box)):
    x[i,:] = K@PI@T_z(tz)@box[i,:] #T_z(tz)@R_z(theta)@R_x(theta)@box[i,:]


plt.figure()
plt.scatter(x[:,0], x[:,1])
plt.show()
