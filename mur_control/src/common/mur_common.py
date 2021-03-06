#!/usr/bin/env python

import numpy as np
import math
from tf.transformations import quaternion_from_euler, euler_from_quaternion, euler_matrix,rotation_matrix

def convert_body_world(pose_rot):
    nita2_t = euler_from_quaternion(pose_rot)
    nita2 = np.array([nita2_t[0],nita2_t[1],nita2_t[2]])
    r = nita2[1]
    p = nita2[0]
    y = nita2[2]
    sr = np.sin(r)
    sp = np.sin(p)
    sy = np.sin(y)
    cr = np.cos(r)
    cp = np.cos(p)
    cy = np.cos(y)
    tp = np.tan(p)
    J = np.array(   [[cy*cp, -sy*cr+cy*sp*sr, sy*sr+cy*cr*sp, 0, 0, 0],
                    [sy*cp, cy*cr+sr*sp*sy, -cy*sr+sp*sy*cr, 0, 0, 0],
                    [-sp, cp*sr, cp*cr, 0, 0, 0],
                    [0, 0, 0, 1, sr*tp, cr*tp],
                    [0, 0, 0, 0, cr, -sr],
                    [0, 0, 0, 0, sr/cp, cr/cp]])
    m_convert = np.array([  [0, 1,  0,  0,  0,  0],
                            [1, 0,  0,  0,  0,  0],
                            [0, 0, -1,  0,  0,  0],
                            [0, 0,  0,  0,  1,  0],
                            [0, 0,  0,  1,  0,  0],
                            [0, 0,  0,  0,  0, -1]])
    J_rotada = np.matmul(m_convert, J)
    return J, np.array([r,p,y])

def rot2(ang):
    ct = np.cos(ang);
    st = np.sin(ang);
    R=np.matrix([[ct,-st],[st,ct]])
    return R

def push_to_pwm(push_value):
    #print push_value
    if push_value > 0:
        params=np.array([0,14.048945,1538.7531]);
    elif push_value < 0:
        params=np.array([0.18721626,17.284769,1460.6878]);
    else:
        push_value = 0;
        params=np.array([0,0,1500]);
    pwm_value = int((params[0]*push_value**2)+(params[1]*push_value)+params[2])
    return pwm_value

def pressure_to_meters(pressure):
    a=-0.000102;
    b=-0.2;
    meters=a*pressure+b;
    return meters

def aruco_to_world(id, rvec, tvec):
    roll = rvec[0][0][0]
    pitch = rvec[0][0][1]
    yaw = rvec[0][0][2]
    tx = tvec[0][0][0]
    ty = tvec[0][0][1]
    tz = tvec[0][0][2]
    rot_matrix = euler_matrix(roll, pitch, yaw)
    M = np.identity(4)
    M[0:3,:] = rot_matrix[0:3,:]
    trans = np.array([[tx],[ty],[tz]])
    M[:3,3] = trans[:3,0]
    if id == 11:
        R = rotation_matrix(-math.pi/2, [1,0,0])
        Mo = np.identity(3)
        Mo = np.matmul(R[:3,:3],trans)
    return Mo
