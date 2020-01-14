import matplotlib.pyplot as plt
import numpy as np 

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
    plt.plot([a[0,0], b[0,0]], [a[1,0], b[1,0]], **args)

def draw_frame(T):
    origin = T@point(0,0,0)
    x = T@point(1,0,0)
    y = T@point(0,1,0)
    z = T@point(0,0,1)
    draw_line(origin, x, color='r')
    plt.text(x[0,0],x[1,0], "X", color='r')
    draw_line(origin, y, color='g')
    plt.text(y[0,0],y[1,0], "Y", color='g')
    draw_line(origin, z, color='b')
    plt.text(z[0,0],z[1,0], "Z", color='b')