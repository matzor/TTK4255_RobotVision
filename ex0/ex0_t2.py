import numpy as np
import matplotlib.pyplot as plt

#Task a-c

theta = np.radians(45)

R_ba = np.array(((np.cos(theta), -np.sin(theta)), 
                (np.sin(theta), np.cos(theta))))

R_ab = np.linalg.inv(R_ba)

p_1a = [1, 0]
p_2b = [1, 0]
p_3b = [0.5, 0.5]

p_1b = R_ab @ p_1a
p_2a = R_ba @ p_2b
p_3a = R_ba @ p_3b

#print(p_1b)
#print(p_2a)
#print(p_3a)

#task d

def point(x,y):
    return np.array([[x], [y], [1]])

def rotate(angle):
    theta = np.radians(angle)
    return np.array([[np.cos(theta), -np.sin(theta), 0], 
                    [np.sin(theta), np.cos(theta), 0],
                    [0, 0, 1]])

def translate(x, y):
    return np.array([[1, 0, x], 
                    [0, 1, y], 
                    [0, 0, 1]])

def draw_line(a, b):
    plt.plot([a[0,0], b[0,0]], [a[1,0], b[1,0]])

def draw_frame(T):
    origin = T@point(0,0)
    draw_line(origin, T@point(1,0))
    draw_line(origin, T@point(0,1))

plt.figure

plt.subplot(131)
plt.axis('scaled')
plt.axis()
plt.grid()
plt.xlim([-1, 5])
plt.ylim([-1, 5])
T1 = rotate(30)@translate(3,0)
draw_frame(T1)

plt.subplot(132)
plt.axis('scaled')
plt.axis()
plt.grid()
plt.xlim([-1, 5])
plt.ylim([-1, 5])
T2 = translate(2,1)@rotate(45)
draw_frame(T2)

plt.subplot(133)
plt.axis('scaled')
plt.axis()
plt.grid()
plt.xlim([-1, 5])
plt.ylim([-1, 5])
T3_1 = rotate(30)@translate(1.5, 0)
draw_frame(T3_1)
T3_2 = translate(0,3)@T3_1@rotate(15)
draw_frame(T3_2)
T3_3 = rotate(-45)@T3_2
draw_frame(T3_3)

plt.show()