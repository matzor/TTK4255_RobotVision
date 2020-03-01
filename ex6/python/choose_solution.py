import numpy as np
from linear_triangulation import *
from camera_matrices import *

def choose_solution(uv1, uv2, K1, K2, Rts):
    """
    Chooses among the rotation and translation solutions Rts
    the one which gives the most points in front of both cameras.
    """

    # todo: Choose the correct solution
    soln = 0
    best = 0
    for i in range(len(Rts)):
        P1, P2 = camera_matrices(K1, K2, Rts[i][0], Rts[i][1])
        pos_z = 0
        for j in range(len(uv1)):
            X = linear_triangulation(uv1[j], uv2[j], P1, P2)
            if X[2] > 0:
                pos_z += 1
        
        if pos_z > best:
            soln = i
    print('Choosing solution %d' % soln)
    return Rts[soln]
