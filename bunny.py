import os
import numpy as np
from PIL import Image

from crt.lights import PointLight
from crt.cameras import PinholeCamera
from crt.rotations import euler_to_rotmat
from crt.static import StaticScene, StaticEntity

# Create the camera object:
camera = PinholeCamera(30, [500,500], [20,20], 
                       position=np.array([0.6,0,0.1]),
                       rotation=euler_to_rotmat('231', np.array([90,10,90]), degrees=True))

# Create a light objects:
sun = PointLight(10, position=np.array([0,0,10]))

# Create static entities:
bunny = StaticEntity("data/bunny.obj", color=[0.5,1,0.5], smooth_shading=True,
                     position=np.array([0,0,-0.1]),
                     rotation=euler_to_rotmat('321', np.array([-120,0,-90]), degrees=True))

floor = StaticEntity("data/cube.obj", color=[0.5,0.5,0.9],
                     position=np.array([0,0,-10.065]), scale=10)

# Create the static scene:
static_scene = StaticScene([bunny, floor])

# Render the image:
if not os.path.exists("bunny_frames"):
    os.makedirs("bunny_frames")

for idx,angle in enumerate(range(0, 360, 6)):
    sun.set_position(np.array([10*np.cos(np.deg2rad(angle)),10*np.sin(np.deg2rad(angle)),3]))
    image = static_scene.render(camera, [sun], min_samples=20, max_samples=60,
                                noise_threshold=0.000001, num_bounces=2)
    Image.fromarray(image.astype(np.uint8)).save('bunny_frames/bunny_{}.png'.format(str(idx).zfill(2)))

    _, normal_image = static_scene.normal_pass(camera, return_image=True)
    Image.fromarray(normal_image.astype(np.uint8)).save('bunny_frames/bunny_normal_{}.png'.format(str(idx).zfill(2)))

    _, depth_image = static_scene.intersection_pass(camera, return_image=True)
    Image.fromarray(depth_image.astype(np.uint8)).save('bunny_frames/bunny_intersection_{}.png'.format(str(idx).zfill(2)))

    _, instance_image = static_scene.instance_pass(camera, return_image=True)
    Image.fromarray(instance_image.astype(np.uint8)).save('bunny_frames/bunny_instance_{}.png'.format(str(idx).zfill(2)))