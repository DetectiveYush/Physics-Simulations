from vpython import *
import numpy as np
from math import *

# Create a canvas
scene = canvas(title="SHM expanded", width=800, height=600)
fps =30
t=0
dt = 1/fps
speed = 1  #units/s
axis_length = pi+1
min_x = axis_length/50
shift_scalar = 2.5*axis_length
shift_vector = vector(2.5*axis_length,0,0)
origin1 = -shift_vector/2
origin2 = origin1 + shift_vector
r0 = 1
labels =[]

# Create Cartesian plane 1 (2D)
def create_cartesian(origin, xlabel, ylabel):
    x_axis = arrow(pos=origin, axis=vector(axis_length, 0, 0), color=color.red, shaftwidth=min_x)
    y_axis = arrow(pos=origin, axis=vector(0, axis_length, 0), color=color.green, shaftwidth=min_x)
    neg_y_axis = arrow(pos=origin, axis=vector(0, -axis_length, 0), color=color.green, shaftwidth=min_x)
    neg_x_axis = arrow(pos=origin, axis=vector(-axis_length, 0, 0), color=color.red, shaftwidth=min_x)
    labels.append(label(pos=origin + vector(axis_length, 0, 0), text=xlabel, xoffset=0, yoffset=10, space=20, height=20, box = False, line = False))
    labels.append(label(pos=origin + vector(0, axis_length, 0), text=ylabel, xoffset=10, yoffset=0, space=20, height=20, box = False, line = False))
    return(x_axis, neg_x_axis, y_axis, neg_y_axis)

(x1_positive, x1_negative, y1_positive, y1_negative) = create_cartesian(origin1, "x", "y")
(x2_positive, x2_negative, y2_positive, y2_negative) = create_cartesian(origin2, "Theta", "r")

#Create objects
object_sphere_cartesian = sphere(pos=vector(-axis_length, r0, 0)+origin1, radius=2*min_x, color=color.orange, make_trail=True, retain = 50)
radius = arrow(pos = origin1, axis = object_sphere_cartesian.pos - origin1, shaftwidth = min_x)
object_sphere_polar = sphere(pos=vector(atan2(radius.axis.y, radius.axis.x), mag(radius.axis), 0)+origin2, radius=2*min_x, color=color.orange, make_trail=True, retain = 50)
radius2 = arrow(pos = vector(object_sphere_polar.pos.x, origin2.y, 0), axis = vector(0, object_sphere_polar.pos.y,0), shaftwidth = min_x)

def radius2update():
    radius2.pos = vector(object_sphere_polar.pos.x, origin2.y, 0)
    radius2.axis = vector(0, object_sphere_polar.pos.y,0)

def polar_update():
    object_sphere_polar.pos.y = mag(radius.axis)
    object_sphere_polar.pos.x = atan2(radius.axis.y, radius.axis.x)
    object_sphere_polar.pos += origin2

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
    
    if speed*t>=2*axis_length:
        reset()
        t = 0