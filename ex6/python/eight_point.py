import numpy as np
from normalize_points import *

def eight_point(uv1, uv2):
    """ Given n >= 8 point matches, (u1 v1) <-> (u2 v2), compute the
    fundamental matrix F that satisfies the equations

        (u2 v2 1)^T * F * (u1 v1 1) = 0

    Args:
        uv1: (n x 2 array) Pixel coordinates in image 1.
        uv2: (n x 2 array) Pixel coordinates in image 2.

    Returns:
        F:   (3 x 3 matrix) Fundamental matrix mapping points in image 1
             to lines in image 2.

    See HZ Ch. 11.2: The normalized 8-point algorithm (p.281).
    """

    # todo: Compute F
    A = np.empty((uv1.shape[0], 9))
    # Use normalized points to build the A matrix
    uv1, T1 = normalize_points(uv1)
    uv2, T2 = normalize_points(uv2)
    for i in range(uv1.shape[0]):
        a = np.array([
            uv2[i,0]*uv1[i,0],
            uv2[i,0]*uv1[i,1],
            uv2[i,0],
            uv2[i,1]*uv1[i,0],
            uv2[i,1]*uv1[i,1],
            uv2[i,1],
            uv1[i,0],
            uv1[i,1],
            1
            ])
        A[i, :] = a
    _, _, v = np.linalg.svd(A, full_matrices=True, compute_uv=True)
    v = v.T
    f = v[:, -1]
    F = np.reshape(f, (3,3))
    F = closest_fundamental_matrix(F)
    # Denormalize F after constraints are enforced
    F = T2.T @ F @ T1
    return F

def closest_fundamental_matrix(F):
    """
    Computes the closest fundamental matrix in the sense of the
    Frobenius norm. See HZ, Ch. 11.1.1 (p.280).
    """
    U, D, V = np.linalg.svd(F, full_matrices=True, compute_uv=True)
    D = np.diag((D[0], D[1], 0))
    F = U @ D @ V
    return F
