import numpy as np

# Task 1a
def central_difference(I):
    """
    Computes the gradient in the u and v direction using
    a central difference filter, and returns the resulting
    gradient images (Iu, Iv) and the gradient magnitude Im.
    """
    kernel = np.array([1/2, 0, -1/2])
    Iu = np.zeros_like(I) # Horizontal
    Iv = np.zeros_like(I) # Vertical
    Im = np.zeros_like(I) # Magnitude
    for row in range(I.shape[0]):
        Iu[row, :] = np.convolve(I[row,:], kernel, 'same')
    for col in range(I.shape[1]):
        Iv[:, col] = np.convolve(I[:, col], kernel, 'same')
    for row in range(I.shape[0]):
        for col in range(I.shape[1]):
            Im[row, col] = np.linalg.norm((Iu[row, col], Iv[row, col]))
    return Iu, Iv, Im

# Task 1b
def blur(I, sigma):
    """
    Applies a 2-D Gaussian blur with standard deviation sigma to
    a grayscale image I.
    """

    # Hint: The size of the kernel, w, should depend on sigma, e.g.
    # w=2*np.ceil(3*sigma) + 1. Also, ensure that the blurred image
    # has the same size as the input image.
    w = 2*np.ceil(3*sigma) + 1
    normal = 1 / (2.0 * np.pi * sigma**2)

    u, v = np.meshgrid(np.arange(-w/2+1, w/2+1),
                       np.arange(-w/2+1, w/2+1))

    # calculating gaussian filter
    kernel = np.exp(-(u**2+v**2) / (2.0*sigma**2)) / normal 
    kern_size = kernel.shape[0]
    result = np.zeros_like(I)

    for i in range(I.shape[0]-(kern_size-1)):
        for j in range(I.shape[1]-(kern_size-1)):
            window = I[i:i+kern_size, j:j+kern_size] * kernel
            result[i, j] = np.sum(window)
    return result

# Task 1c
def extract_edges(Iu, Iv, Im, threshold):
    """
    Returns the u and v coordinates of pixels whose gradient
    magnitude is greater than the threshold.
    """

    # This is an acceptable solution for the task (you don't
    # need to do anything here). However, it results in thick
    # edges. If you want better results you can try to replace
    # this with a thinning algorithm as described in the text.
    v,u = np.nonzero(Im > threshold)
    theta = np.arctan2(Iv[v,u], Iu[v,u])
    return u, v, theta

def rgb2gray(I):
    """
    Converts a red-green-blue (RGB) image to grayscale brightness.
    """
    return 0.2989*I[:,:,0] + 0.5870*I[:,:,1] + 0.1140*I[:,:,2]
