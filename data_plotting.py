import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import time

# Load data from file and remove rows containing 'None' values
data = np.genfromtxt('pollutant_log.txt', delimiter=',', dtype=float, missing_values='None', filling_values=np.nan)
data = data[~np.isnan(data).any(axis=1)]

# Calculate the mean and standard deviation of longitude and latitude
mean_longitude = np.mean(data[:, 0])
std_longitude = np.std(data[:, 0])
mean_latitude = np.mean(data[:, 1])
std_latitude = np.std(data[:, 1])

# Define a function to check if a latitude or longitude value is an outlier
def is_outlier(latitude, longitude, std_multiplier):
    return (abs(latitude - mean_latitude) > std_multiplier * std_latitude) or (abs(longitude - mean_longitude) > std_multiplier * std_longitude)

# Create a boolean array indicating which rows to keep
std_multiplier = 2 # adjust this value to increase or decrease the outlier tolerance
keep_rows = np.array([not is_outlier(lat, lon, std_multiplier) for lat, lon in zip(data[:, 1], data[:, 0])])

# Apply the boolean array to the data to keep only the non-outlier rows
data = data[keep_rows]

# Separate data into separate arrays
longitude = data[:, 0]
latitude = data[:, 1]
pollution = data[:, 2]
print(len(pollution))
# Reshape pollution into a 2D array

def twoD_Gaussian(xy, amplitude, xo, yo, sigma_x, sigma_y, theta, offset):
    x, y = xy
    xo = float(xo)
    yo = float(yo)
    a = (np.cos(theta)**2)/(2*sigma_x**2) + (np.sin(theta)**2)/(2*sigma_y**2)
    b = -(np.sin(2*theta))/(4*sigma_x**2) + (np.sin(2*theta))/(4*sigma_y**2)
    c = (np.sin(theta)**2)/(2*sigma_x**2) + (np.cos(theta)**2)/(2*sigma_y**2)
    g = offset + amplitude*np.exp( - (a*((x-xo)**2) + 2*b*(x-xo)*(y-yo)
                            + c*((y-yo)**2)))
    return g


# fit a gaussian to the data
popt = curve_fit(twoD_Gaussian, (longitude, latitude), pollution, maxfev=5000, p0=[10, 2, 2, 1, 1, 0, 1])
# fitted parameters 
f_p = popt[0]

# create a mesh for the grid (only for plotting)
x_plot = np.arange(min(longitude), max(longitude), 0.01)
y_plot = np.arange(min(latitude), max(latitude), 0.01)
X, Y = np.meshgrid(longitude, latitude)
Z = twoD_Gaussian((X, Y), f_p[0], f_p[1], f_p[2], f_p[3], f_p[4], f_p[5], f_p[6])

print('starting plot')
# Create a surface plot
fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis')
ax.scatter(longitude, latitude, data, marker='o', color='red', label='Measured Pollution')

# ax = fig.add_subplot(111, projection='3d')
# longitude_mesh, latitude_mesh = np.meshgrid(longitude, latitude)
# ax.plot_surface(longitude_mesh, latitude_mesh, gaussian, cmap='viridis')

ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Pollution percentage')
ax.set_title('Pollution Map')
plt.show()