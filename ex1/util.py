import matplotlib.pyplot as plt
import numpy as np 

def point(x, y, z):
    return np.array([[x], [y], [z], [1]])

#rotation matrices
def T_xyz(tx,ty,tz):
    Tz = np.identity(4)
    Tz[0, 3] = tx
    Tz[1, 3] = ty
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

def draw_frame(T, KPI, length_of_axis):
    l = length_of_axis
    axis = np.array([[0,0,0,1], [1*l,0,0,1],[0,1*l,0,1],[0,0,1*l,1]])
    axis = T@axis.T
    scale_axis = 1/axis[2,:]
    X = KPI@axis
    X = scale_axis * X
    origin = X[:,0]
    x = X[:,1]
    y = X[:,2]
    z = X[:,3]
    draw_line(origin, x, color='r')
    plt.text(x[0],x[1], "X", color='r')
    draw_line(origin, y, color='g')
    plt.text(y[0],y[1], "Y", color='g')
    draw_line(origin, z, color='b')
    plt.text(z[0],z[1], "Z", color='b')