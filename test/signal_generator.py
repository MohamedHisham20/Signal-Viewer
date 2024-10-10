import numpy as np
import csv
import os

# Parameters
num_points = 1000  # Number of data points
x_values = np.linspace(0, 2 * np.pi, num_points)  # Generate x values from 0 to 2*pi
y_values = np.sin(x_values)  # Compute the sine of each x value

# File name
file_path = os.path.join(os.getcwd(), 'signal.csv')


# Write to CSV
with open(file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['x', 'y'])  # Write header
    for x, y in zip(x_values, y_values):
        writer.writerow([x, y])

