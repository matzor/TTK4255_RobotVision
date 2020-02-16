import numpy as np
import matplotlib.pyplot as plt
from common1 import *
from common2 import *

edge_threshold = 1 # todo: choose an appropriate value
blur_sigma     = 1 # todo: choose an appropriate value
filename       = '../data/image1_und.jpg'

I_rgb      = plt.imread(filename)
I_rgb      = I_rgb/255.0
I_gray     = rgb2gray(I_rgb)
I_blur     = blur(I_gray, blur_sigma)
Iu, Iv, Im = central_difference(I_blur)
u,v,theta  = extract_edges(Iu, Iv, Im, edge_threshold)

#
# Task 2a: Compute accumulator array H
#
bins      = 1000
rho_max   = 1000
rho_min   = -1000
theta_max = np.pi 
theta_min = -np.pi 


# Tip: Use histogram2d for task 2a
rho = u*np.cos(theta) + v*np.sin(theta)
print("min rho:", rho[np.argmin(rho)], "max rho:", rho[np.argmax(rho)], "shape rho:", rho.shape)
print("theta rho:", theta[np.argmin(theta)], "max theta:", theta[np.argmax(theta)], "shape theta:", theta.shape)
H, _, _ = np.histogram2d(theta, rho, bins=bins, range=[[theta_min, theta_max], [rho_min, rho_max]])
H = H.T # Make rows be rho and columns be theta (see documentation)

#
# Task 2b: Find local maxima
#
line_threshold = 15
window_size = 10 
peak_rows,peak_cols = extract_peaks(H, window_size, line_threshold)

#
# Task 2c: Convert peak (row, column) pairs into (theta, rho) pairs.
#
#peak_theta = [0, 0.2, 0.5, 0.7] # Placeholder to demonstrate use of draw_line
#peak_rho   = [10, 100, 300, 500] # Placeholder to demonstrate use of draw_line

rho_step = (rho_max - rho_min) / bins
theta_step = (theta_max - theta_min) / bins
peak_rho = np.zeros(len(peak_rows))
peak_theta = np.zeros(len(peak_cols))

for i in range(len(peak_rows)):
    peak_rho[i] = rho_min + peak_rows[i] * rho_step
    peak_theta[i] = theta_max + peak_cols[i] * theta_step


plt.figure(figsize=[6,8])
plt.subplot(211)
plt.imshow(H, extent=[theta_min, theta_max, rho_min, rho_max], aspect='auto')
plt.xlabel('$\\theta$ (radians)')
plt.ylabel('$\\rho$ (pixels)')
plt.colorbar(label='Votes')
plt.title('Hough transform histogram')
plt.subplot(212)
plt.imshow(I_rgb)
plt.xlim([0, I_rgb.shape[1]])
plt.ylim([I_rgb.shape[0], 0])
for i in range(len(peak_theta)):
    draw_line(peak_theta[i], peak_rho[i], color='yellow')
plt.tight_layout()
plt.savefig('out2.png')
plt.show()
