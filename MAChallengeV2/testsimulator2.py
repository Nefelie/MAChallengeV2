

import math
from math import radians, degrees, sin, cos, sqrt, atan2
import matplotlib.pyplot as plt
import numpy as np
from LoadWPL import load_wpl
from LOS_guidance import DMM_to_DEG

def range_converter(latitude, longitude, range_km):
    # Convert latitude and longitude to radians
    lat1 = radians(latitude)
    lon1 = radians(longitude)

    # Earth's radius in kilometers
    radius = 6371.01

    # Calculate the angular distance in radians
    angular_distance = range_km / radius

    # Calculate the new latitude in degrees
    lat2 = degrees(math.asin(sin(lat1) * cos(angular_distance) +
                 cos(lat1) * sin(angular_distance) * cos(0)))

    # Calculate the new longitude in degrees
    lon2 = degrees(lon1 + atan2(sin(0) * sin(angular_distance) * cos(lat1),
                     cos(angular_distance) - sin(lat1) * sin(lat2)))

    return lat2, lon2


# Define the initial coordinate and range
init_lat = 50.845 #40.7128
init_lon = 0.7459 #-74.0060



wp = [[init_lat, init_lon]]  # initialize with the initial coordinate

tracks = load_wpl('data.txt')
for track in tracks:
    for waypoint_dmm in track:
        #wp.append([DMM_to_DEG(waypoint_dmm)[0], DMM_to_DEG(waypoint_dmm)[1]])  append the waypoint as a list of two coordinates
        wp.append(DMM_to_DEG(waypoint_dmm))

print(wp)



# Create an empty plot with axis labels
fig, ax = plt.subplots()
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

# Set the axis limits and turn on interactive plotting
plt.ion()

# Create an empty list to store the data
data_lat = np.arange(init_lat - lat_range, init_lat + lat_range, 0.01)
data_lon = np.arange(init_lon - lon_range, init_lon + lon_range, 0.01)
theta = np.arange(1, 31.4, 0.1)
speed = np.arange(1, 31.4, 0.1)
error = np.arange(1, 31.4, 0.1)

# Initialize the time and frequency variables
t = 0
freq = 1

# Define a function to handle the keyboard interrupt event
def on_key_press(event):
    if event.key == 'p':
        fig.canvas.stop_event_loop()

# Connect the keyboard interrupt handler to the plot window
fig.canvas.mpl_connect('key_press_event', on_key_press)

# waypoint
#wp = [init_lat, init_lon + 0.02]

for point in wp:
        ax.plot(point[0], point[1], marker='o', markersize=10)


# Add the new point to the list
plt.ylim([init_lat - lat_range/2, init_lat + lat_range/2])
plt.xlim([init_lon - lon_range/2, init_lon + lon_range/2])

# Continuously generate new data and update the plot
while True:

    # Generate a new point on the sine wave
    y = math.sin(2 * math.pi * freq * t)

    ax.plot(data_lon[t], data_lat[t], color='r', markersize=10, marker='1')

    # plt.arrow(data_x[t],data_y[t], 0.5, 0.5, head_length=0.5)
    plt.annotate("", xy=(data_lon[t]+np.cos(theta[t]), data_lat[t]+np.sin(theta[t])), xytext=(data_lon[t], data_lat[t]),
                arrowprops=dict(arrowstyle="->"))



    # Redraw the plot and pause briefly to allow the plot to update
    plt.text(init_lon + lon_range * 0.6, init_lat + lat_range * 0.9, f"Heading: {theta[t]:.2f} rad")
    plt.text(init_lon + lon_range * 0.6, init_lat + lat_range * 0.8, f"Speed: {speed[t]:.2f} kts")
    plt.text(init_lon + lon_range * 0.6, init_lat + lat_range * 0.7, f"Cross Track Error: {error[t]:.2f} m")
    plt.draw()
    plt.pause(0.01)

    # Increment the time variable
    t += 1
    

    # Check if a keyboard interrupt event has occurred
    if not plt.fignum_exists(fig.number):
        break

    # Clear the plot to allow for a live update
    ax.cla()
# Turn off interactive plotting
plt.ioff()

# Show the final plot
plt.show()