from vpython import *
import numpy as np

# Create a canvas
scene = canvas(title="SHM expanded", width=800, height=600)
axis_length = 1.5
shift = axis_length*2
origin1 =  vector(-shift,0,0)
origin2 = origin1+vector(shift, 0, 0)
t = 0 # Initialize time
fps=30
dt = 1/fps  # Time step
rpm = 30
w =2*pi*rpm/60 #angular frequency(speed)

# Create Cartesian plane 1 (2D)

x_axis = arrow(pos=origin1, axis=vector(axis_length, 0, 0), color=color.red, shaftwidth=0.02)
y_axis = arrow(pos=origin1, axis=vector(0, axis_length, 0), color=color.green, shaftwidth=0.02)
neg_y_axis = arrow(pos=origin1, axis=vector(0, -axis_length, 0), color=color.green, shaftwidth=0.02)
neg_x_axis = arrow(pos=origin1, axis=vector(-axis_length, 0, 0), color=color.red, shaftwidth=0.02)

x2_axis = arrow(pos=origin2, axis=vector(axis_length, 0, 0), color=color.red, shaftwidth=0.02)
y2_axis = arrow(pos=origin2, axis=vector(0, axis_length, 0), color=color.green, shaftwidth=0.02)
neg_y2_axis = arrow(pos=origin2, axis=vector(0, -axis_length, 0), color=color.green, shaftwidth=0.02)

# Create a circular path using curve
circle_path = curve(pos = origin1, color=color.blue, radius=0.01)
theta_values = np.linspace(0, 2*np.pi, 100)
for theta in theta_values:
    x = np.cos(theta)+origin1.x
    y = np.sin(theta)+origin1.y
    circle_path.append(vector(x, y, 0))

# Create a small sphere to represent the object
object_sphere = sphere(pos=vector(1, 0, 0)+origin1, radius=0.05, color=color.orange, make_trail=False)
acceleration = arrow(pos = object_sphere.pos, axis = -vector(0, object_sphere.pos.y, 0))

#Create indicator line
line = curve(pos=[object_sphere.pos, vector(shift, object_sphere.pos.y, 0)+origin1], color=color.cyan, radius=0.02)
right_indicator_sphere = sphere(pos=vector(shift, object_sphere.pos.y, 0), radius=0.05, color=color.orange, make_trail=False)

def update_line():
    line.clear()
    line.append(object_sphere.pos)
    line.append(vector(0, object_sphere.pos.y, 0)+origin2)
    right_indicator_sphere.pos = vector(0, object_sphere.pos.y, 0)+origin2

#Create Sinusoid
sinusoid = curve(os =[origin1, origin2], retain = round(pi/dt))


def update_sinusoid():
    sinusoid.origin += vector(dt, 0, 0)
    sinusoid.append(right_indicator_sphere.pos - vector(t, 0, 0))

# Animation loop: Move the sphere along the circular path

while True:
    rate(fps)  # Controls the speed of the animation (50 frames per second)
    
    # Parametric equations for circular motion
    x = np.cos(w*t)+origin1.x
    y = np.sin(w*t)+origin1.y

    # Update the sphere's position
    object_sphere.pos = vector(x, y, 0)
    acceleration.pos = object_sphere.pos
    acceleration.axis = -vector(0, object_sphere.pos.y, 0)
    update_line()
    update_sinusoid()

    #cyclic time to avoid memory leak
    t += dt
    #if w*t >= 2*pi:
    #    t = 0 
