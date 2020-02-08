import numpy as np

K                  = np.loadtxt('../data/cameraK.txt')
p_model            = np.loadtxt('../data/model.txt')
platform_to_camera = np.loadtxt('../data/pose.txt')
P = np.array(   [[1,0,0,0],
                [0,1,0,0],
                [0,0,1,0]])

def residuals(uv, weights, yaw, pitch, roll):

    # Helicopter model from Exercise 1 (you don't need to modify this).
    base_to_platform = translate(0.1145/2, 0.1145/2, 0.0)@rotate_z(yaw)
    hinge_to_base    = translate(0, 0, 0.325)@rotate_y(pitch)
    arm_to_hinge     = translate(0, 0, -0.0552)
    rotors_to_arm    = translate(0.653, 0, -0.0312)@rotate_x(roll)
    base_to_camera   = platform_to_camera@base_to_platform
    hinge_to_camera  = base_to_camera@hinge_to_base
    arm_to_camera    = hinge_to_camera@arm_to_hinge
    rotors_to_camera = arm_to_camera@rotors_to_arm

    #
    # Task 1a: Implement the rest of this function
    #

    uv_temp = np.empty([4, uv.shape[0]])
    # First 3 markers are transformed to arm-frame, last 4 markers to rotor-frame
    uv_temp[:, 0:3] = arm_to_camera @ p_model[0:3, :].T
    uv_temp[:, 3:]  = rotors_to_camera @ p_model[3:, :].T
    
    # Multiply camera matrix, projection matrix
    uv_hat = K @ P @ uv_temp
    uv_hat = uv_hat.T

    # Normalize 1/z
    for row in range(uv_hat.shape[0]):
        uv_hat[row, :] = uv_hat[row, :] / uv_hat[row, 2]
   
    point_diff = uv_hat[:, 0:2] - uv
    # Find norm and remove not-detected points
    res = np.multiply(np.linalg.norm(point_diff, axis=1), weights) 


    return res

def normal_equations(uv, weights, yaw, pitch, roll):
    #
    # Task 1b: Compute the normal equation terms
    #
    
    r = residuals(uv, weights, yaw, pitch, roll)
    theta = [yaw, pitch, roll]
    epsilon = 1e-7                      # "small change" in x
    
    J = np.empty([len(r), len(theta)])  # height of r, width of theta
    
    # Calculate gradient using finite difference method
    for i in range(len(theta)):
        _theta = theta
        _theta[i] += epsilon            # adding "small change" to angle i
        r_e = residuals(uv, weights, _theta[0], _theta[1], _theta[2])
        J[:, i] = (r_e - r) / epsilon

    JTJ = J.T @ J 
    JTr = J.T @ r
    return JTJ, JTr

def gauss_newton(uv, weights, yaw, pitch, roll):
    #
    # Task 1c: Implement the Gauss-Newton method
    #
    max_iter = 100
    step_size = 0.25
    theta = np.array([yaw, pitch, roll])
    for iter in range(max_iter):
        JTJ, JTr = normal_equations(uv, weights, theta[0], theta[1], theta[2])
        delta = np.linalg.solve(JTJ, -JTr)
        theta += step_size*delta
    return theta[0], theta[1], theta[2]

def levenberg_marquardt(uv, weights, yaw, pitch, roll):
    #
    # Task 2a: Implement the Levenberg-Marquardt method
    #
    max_iter = 100
    step_size = 0.25
    lam = 1e-3
    precision = 1e-3
    error = 0

    theta = np.array([yaw, pitch, roll])
    JTJ, JTr = normal_equations(uv, weights, theta[0], theta[1], theta[2])
    D = np.eye(3) * np.average(np.diag(JTJ))
    _theta = theta

    #print("NEW IMAGE: ")
    
    for iter in range(max_iter):
        JTJ, JTr = normal_equations(uv, weights, theta[0], theta[1], theta[2])
        delta = np.linalg.solve((JTJ + lam * D), -JTr)
        _theta = theta + step_size*delta
        _error = np.linalg.norm(_theta - theta)
        theta = _theta

        # termination criteria
        if _error < precision:
            break
        # Calculate new lambda
        if _error < error:
            lam = lam/10
        else:
            lam = lam*10
        
        error = _error
        #print("Iteration %i Theta: %f, %f, %f, Lambda: %f" %(iter, theta[0], theta[1], theta[2], lam))
        

    return theta[0], theta[1], theta[2]

def rotate_x(radians):
    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[1, 0, 0, 0],
                     [0, c,-s, 0],
                     [0, s, c, 0],
                     [0, 0, 0, 1]])

def rotate_y(radians):
    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[ c, 0, s, 0],
                     [ 0, 1, 0, 0],
                     [-s, 0, c, 0],
                     [ 0, 0, 0, 1]])

def rotate_z(radians):
    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[c,-s, 0, 0],
                     [s, c, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])

def translate(x, y, z):
    return np.array([[1, 0, 0, x],
                     [0, 1, 0, y],
                     [0, 0, 1, z],
                     [0, 0, 0, 1]])
