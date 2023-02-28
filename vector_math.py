import numpy as np
def rotate(vector,angle):
    rotation_matrix = np.array([
        np.array([np.cos(angle),np.sin(angle)]),
        np.array([-np.sin(angle),np.cos(angle)])
    ])
    return rotation_matrix@vector

def signof(x):
    if (x<0):
        return -1
    if (x>0):
        return 1
    return 0

def angle(v1,v2):
    return-np.arccos(np.dot(v1,v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)) ) * signof(np.cross(v1,v2))

