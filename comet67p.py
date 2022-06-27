import os
import numpy as np
from PIL import Image

import spiceypy as spice

from crt.cameras import SimpleCamera
from crt.lidars import SimpleLidar
from crt.lights import PointLight
from crt import BodyFixedGroup, BodyFixedEntity

# Number of measurements to take:
number_of_measurements = 30
# number_of_measurements = 300 #(This is what was used to generate the .GIF)

# Load the appropraite spice kernels:
spice.furnsh('comet67p.tm')

# Create the camera object:
camera = SimpleCamera(60, [500,500], [20,20], z_positive=True, 
                      name='ROSETTA', frame='ROS_SPACECRAFT', 
                      origin='CHURYUMOV-GERASIMENKO')

# Create a light objects:
sun_intensity = 2e16
sun = PointLight(sun_intensity, name='SUN', origin='CHURYUMOV-GERASIMENKO')

# Load body fixed geometries:
comet_body = BodyFixedEntity("data/67p.obj", smooth_shading=True)

# Create the Comet scene:
comet_scene = BodyFixedGroup(comet_body, 
                             name='CHURYUMOV-GERASIMENKO',
                             frame='67P/C-G_CK', origin='CHURYUMOV-GERASIMENKO')

et_start = spice.str2et('2016 MAR 2 12:00:00')
et_end   = spice.str2et('2016 MAR 4 12:00:00')

ets = np.linspace(et_start, et_end, num=number_of_measurements)

if not os.path.exists("output_comet67p"):
    os.makedirs("output_comet67p")

# Render for the trajectory:
# print('Rendering {} frames...'.format(ets.size))
# for idx, et in enumerate(ets):
#     # Set the pose (using SPICE) for all objects:
#     camera.spice_pose(et)
#     sun.spice_position(et)
#     comet_scene.spice_pose(et)

#     # Render and save the current image:
#     image = comet_scene.render(camera, sun, min_samples=20, max_samples=100,
#                                noise_threshold=0.000001, num_bounces=2)
#     Image.fromarray(image.astype(np.uint8)).save('output_comet67p/frame_{}.png'.format(str(idx).zfill(3)))


# Create lidar model in the comet frame:
lidar = SimpleLidar(z_positive=True, 
                    name='ROSETTA', frame='ROS_SPACECRAFT', 
                    origin='CHURYUMOV-GERASIMENKO',ref='67P/C-G_CK')

# Generate a batch of Lidar measurements (up to 100,000):
ets = np.linspace(et_start, et_end, num=100000)
lidar.batch_spice_pose(ets)

# Reset comet frame:
comet_scene.set_pose(np.zeros(3),np.eye(3))

# Simulate Lidar:
print('Simulating {} lidar pulses...'.format(ets.size))
altitudes = comet_scene.batch_simulate_lidar(lidar)

# Remove the zeros (Lidar detected no intersection):
remove_inds = np.where(altitudes == 0)
alts_plt = np.delete(altitudes, remove_inds)
ets_plt  = np.delete(ets, remove_inds)

# Plot with matplotlib (if you have it installed):
# import matplotlib.pyplot as plt
# fig, ax = plt.subplots()
# ax.plot(ets_plt, alts_plt,'.k',markersize=1)
# ax.set(xlabel='Ephemeris Time (seconds)', 
#        ylabel='Altitude (km)',
#        title='LiDAR Simulation')
# ax.grid()
# fig.savefig("lidar.png")
# plt.show()