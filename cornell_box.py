import numpy as np
from PIL import Image

from crt.lighting import PointLight, SquareLight
from crt.cameras import PinholeCamera
from crt.passes import normal_pass, depth_pass, instance_pass
from crt.rotations import euler_to_rotmat
from crt import Entity, render

# Create the camera object:
camera = PinholeCamera(30, [500,500], [19.5,19.5], position=np.array([4,0,0]),
                       rotation=euler_to_rotmat('231', np.array([90,0,90]), degrees=True))

# Create a light objects:
light = PointLight(3, position=np.array([4,2.2,1.5]))
top_light = SquareLight(0.05, [0.2,0.2], position=np.array([0.0, 0.0, 0.99]))

# Load all geometry:
floor      = Entity("data/cube.obj", position=np.array([0,0,-2]))
ceiling    = Entity("data/cube.obj", position=np.array([0,0,2]))
back_wall  = Entity("data/cube.obj", position=np.array([-2,0,0]))
left_wall  = Entity("data/cube.obj", position=np.array([0,-2,0]), color=[1, 0.1, 0.1])
right_wall = Entity("data/cube.obj", position=np.array([0,2,0]),  color=[0.1, 1, 0.1])
ball = Entity("data/ball.obj", smooth_shading=True, color=[0.5,0.5,0.9],
              position=np.array([0.3, 0.6, -.6]), scale=0.4)
box = Entity("data/tall_box.obj", scale=0.27, position = np.array([-.4, -0.4, -0.8]),
             rotation=euler_to_rotmat('123',np.array([0,0,70]), degrees=True))

# Store all lights and objects into lists:
lights   = [light, top_light]
entities = [floor, ceiling, back_wall, left_wall, right_wall, ball, box]

# Render the image:
image = render(camera, lights, entities, min_samples=20, max_samples=100, 
               noise_threshold=0.000001, num_bounces=2)
Image.fromarray(image.astype(np.uint8)).save('cornell_box.png')

# Get the intersections:
intersections, depth_image = depth_pass(camera, entities, return_image=True)
Image.fromarray(depth_image.astype(np.uint8)).save('cornell_box_depth.png')

# Get the instances:
instances, instance_image = instance_pass(camera, entities, return_image=True)
Image.fromarray(instance_image.astype(np.uint8)).save('cornell_box_instance.png')

# Get the normals:
normal_image = normal_pass(camera, entities)
Image.fromarray(normal_image.astype(np.uint8)).save('cornell_box_normals.png')