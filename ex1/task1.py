import matplotlib.pyplot as plt
import numpy as np 

box = np.loadtxt('box.txt')
#box[:, 2] += box[:,2] + 5   #translates box 5m

#rotation matrices
tz = 5
theta = 30

Tz = np.identity(4)
Tz[2, 3] = tz
print(Tz)


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

for i in range(len(box)):
    x[i,:] = K@PI@Tz@box[i,:]

plt.figure()
plt.scatter(x[:,0], x[:,1])
plt.show()
