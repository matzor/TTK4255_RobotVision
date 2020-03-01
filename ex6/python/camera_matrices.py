import numpy as np

def camera_matrices(K1, K2, R, t):
    """ Computes the projection matrix for camera 1 and camera 2.

    Args:
        K1,K2: Intrinsic matrix for camera 1 and camera 2.
        R,t: The rotation and translation mapping points in camera 1 to points in camera 2.

    Returns:
        P1,P2: The projection matrices with shape 3x4.
    """

    # todo: compute the correct P1 and P2
    PI = np.zeros((3,4))
    PI[:, :3] = np.eye(3)
    P1 = K1 @ PI

    PI2 = np.empty((3,4))
    PI2[:, :3] = R[:,:]
    PI2[:, 3]  = t[:]
    P2 = K2 @ PI2

    return P1, P2
