import matplotlib.pyplot as plt
import yaml 
from LOS_guidance import LOS_latlon, call_distance, DMM_to_DEG
from LoadWPL import load_wpl


# Load the YAML file
with open('boat_setup.yaml', 'r') as file:
    yaml_data = yaml.safe_load(file)

# Access the value of the variable
initial_coordinates = yaml_data['hyper_parameters']['initial_position']
max_range = load_wpl('output.txt')

waypoints_deg = []
for track in max_range:
    # going through each waypoint in the track
    for waypoint_dmm in track:
        waypoints_deg.append([DMM_to_DEG(waypoint_dmm)[0], DMM_to_DEG(waypoint_dmm)[1]])

print(waypoints_deg)
print(initial_coordinates)

x_max = max(coord[0] for coord in waypoints_deg)
y_max = max(coord[1] for coord in waypoints_deg)

x_min = min(coord[0] for coord in waypoints_deg)
y_min = min(coord[1] for coord in waypoints_deg)
waypoint_n = 15 # number of steps done in the initial search function
area_length = max(x_max - x_min, y_max - y_min) # length of total area of square of search pattern

def generate_spiral_square(initial_coordinates, waypoint_n, area_length):
    waypoints = []
    x, y = inital_coordinates
    for i in range(waypoint_n):
        # calculate the next x and y coordinates
        if i % 4 == 0:
            x += area_length
        elif i % 4 == 1:
            y -= area_length
        elif i % 4 == 2:
            x -= area_length
        else:
            y += area_length
        # add the new waypoint to the list
        waypoints.append((x, y))
        # increase the length for the next side
        area_length += 10
    return waypoints

# generate the waypoints
waypoints = generate_spiral_square(initial_coordinates, waypoint_n, area_length)
print(waypoints)

# plot the waypoints
x_values = [x for x, y in waypoints]
y_values = [y for x, y in waypoints]






# def convert_to_MMWPL(lst):
#     message = ""
#     for i, tpl in enumerate(lst):
#         lat = "{:.6f}".format(abs(tpl[0]))
#         lat_dir = "N" if tpl[0] >= 0 else "S"
#         lon = "{:.6f}".format(abs(tpl[1]))
#         lon_dir = "E" if tpl[1] >= 0 else "W"
#         while len(lon.split(".")[0]) < 4:
#             lon = "0" + lon
#         message += f"$MMWPL,{lat},{lat_dir},0{lon},{lon_dir},WPT {i+1}\n"
#     return message


message = convert_to_MMWPL(waypoints)

print(message)
with open("output.txt", "w") as f:
   f.write(message)