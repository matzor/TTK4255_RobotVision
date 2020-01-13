import matplotlib.pyplot as plt
import numpy as np 

box = np.loadtxt('box.txt')

plt.figure()
plt.scatter(box[:,0], box[:,1])
plt.show()
