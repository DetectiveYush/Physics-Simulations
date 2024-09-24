from vpython import *
import numpy as np
from math import *

# Create a canvas
scene = canvas(title="SHM expanded", width=1080, height=600)
fps =30
t=0
dt = 1/fps
speed = 1  #units/s
axis_length = pi+1
min_x = axis_length/50
shift_scalar = 2.5*axis_length
shift_vector = vector(2.5*axis_length,0,0)
origin1 = -shift_vector
origin2 = origin1 + 2*shift_vector
origin3 = origin1 + shift_vector
r0 = 1
labels =[]

# Cartesian plane creation function(2D)
def create_cartesian(origin, xlabel, ylabel, title):
    x_axis = arrow(pos=origin, axis=vector(axis_length, 0, 0), color=color.red, shaftwidth=min_x)
    y_axis = arrow(pos=origin, axis=vector(0, axis_length, 0), color=color.green, shaftwidth=min_x)
    neg_y_axis = arrow(pos=origin, axis=vector(0, -axis_length, 0), color=color.green, shaftwidth=min_x)
    neg_x_axis = arrow(pos=origin, axis=vector(-axis_length, 0, 0), color=color.red, shaftwidth=min_x)
    labels.append(label(pos=origin + vector(axis_length, 0, 0), text=xlabel, xoffset=0, yoffset=10, space=20, height=20, box = False, line = False))
    labels.append(label(pos=origin + vector(0, axis_length, 0), text=ylabel, xoffset=10, yoffset=0, space=20, height=20, box = False, line = False))
    labels.append(label(pos=origin + vector(-axis_length, 1.5*axis_length, 0), text=title, xoffset=10, yoffset=0, space=20, height=20, box = False, line = False))
    return(x_axis, neg_x_axis, y_axis, neg_y_axis)

#Create Cartesian planes (2D)
(x1_positive, x1_negative, y1_positive, y1_negative) = create_cartesian(origin1, "x", "y", "Observer can see x,y")
(x2_positive, x2_negative, y2_positive, y2_negative) = create_cartesian(origin2, "Theta", "r", "Observer can see r, theta")
(x3_positive, x3_negative, y3_positive, y3_negative) = create_cartesian(origin3, "x", "y", "Observer can only see r")

#variables for later use
positive_x = x1_positive.axis
positive_y = y1_positive.axis
negative_x = x1_negative.axis
negative_y = y1_negative.axis

#rotation function(2D)
def rotate(rotation_vector, rotation_angle):
    rotated_vector = (1,1,0)
    rotated_vector.x = rotation_vector.x
    rotated_vector.y = rotation_vector.y
    rotated_vector.x = rotation_vector.x * np.cos(rotation_angle) - rotation_vector.y * np.sin(rotation_angle)
    rotated_vector.y = rotation_vector.x * np.sin(rotation_angle) + rotation_vector.y * np.cos(rotation_angle)
    rotation_vector.x = rotated_vector.x
    rotation_vector.y = rotated_vector.y

#Create objects
object_sphere_cartesian = sphere(pos=vector(-axis_length, r0, 0)+origin1, radius=2*min_x, color=color.orange, make_trail=True, retain = 50)
radius = arrow(pos = origin1, axis = object_sphere_cartesian.pos - origin1, shaftwidth = min_x)
object_sphere_polar = sphere(pos=vector(atan2(radius.axis.y, radius.axis.x), mag(radius.axis), 0)+origin2, radius=2*min_x, color=color.orange, make_trail=True, retain = 50)
radius2 = arrow(pos = vector(object_sphere_polar.pos.x, origin2.y, 0), axis = vector(0, object_sphere_polar.pos.y,0), shaftwidth = min_x)
object_sphere_observer = sphere(pos=vector(0, mag(radius.axis), 0)+origin3, radius=2*min_x, color=color.orange, make_trail=True, retain = 50)
radius3 = arrow(pos = origin3, axis = vector(0, object_sphere_polar.pos.y,0), shaftwidth = min_x)


def radius2update():
    radius2.pos = vector(object_sphere_polar.pos.x, origin2.y, 0)
    radius2.axis = vector(0, object_sphere_polar.pos.y,0)

def polar_update():
    object_sphere_polar.pos.y = mag(radius.axis)
    object_sphere_polar.pos.x = atan2(radius.axis.y, radius.axis.x)
    object_sphere_polar.pos += origin2

def rotating_frame_update():
    rotation_angle = atan2(radius.axis.y, radius.axis.x)

    x3_positive.axis = vector(-positive_y.y*sin(-rotation_angle), positive_y.y*cos(-rotation_angle),0)
    x3_negative.axis = vector(-negative_y.y*sin(-rotation_angle), negative_y.y*cos(-rotation_angle),0)
    y3_positive.axis = vector(negative_x.x*cos(-rotation_angle), negative_x.x*sin(-rotation_angle), 0)
    y3_negative.axis = vector(positive_x.x*cos(-rotation_angle), positive_x.x*sin(-rotation_angle), 0)

    #Calculated manually, fix later
    labels[6].pos = origin3 + x3_positive.axis
    labels[7].pos = origin3 + y3_positive.axis
    radius3.axis = vector(0, mag(radius.axis), 0)
    object_sphere_observer.pos.y = radius3.axis.y

    
rotating_frame_update()

def reset():
    object_sphere_cartesian.pos = vector(-axis_length, r0, 0)+origin1
    object_sphere_cartesian.clear_trail()
    object_sphere_polar.pos = vector(-pi, axis_length, 0)+origin2
    object_sphere_polar.clear_trail()
    radius.axis = object_sphere_cartesian.pos - origin1
    polar_update()
    object_sphere_polar.clear_trail()
    radius2update()
    

while True:
    rate(fps)
    t+=dt
    object_sphere_cartesian.pos += vector(speed*dt,0,0)
    radius.axis = object_sphere_cartesian.pos - origin1
    polar_update()
    radius2update()
    rotating_frame_update()
    
    if speed*t>=2*axis_length:
        reset()
        t = 0