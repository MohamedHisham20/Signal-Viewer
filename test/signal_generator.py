import numpy as np
import csv

# Parameters
num_points = 1000
t = np.linspace(0, 10, num_points)

# Generate a synthetic ECG signal
def generate_ecg(t):
    return 1.5 * np.sin(2 * np.pi * 1.0 * t) + 0.5 * np.sin(2 * np.pi * 3.0 * t) + 0.2 * np.random.randn(len(t))

ecg_values = generate_ecg(t)

# File path
csv_file_path = 'ecg_signal.csv'

# Write to CSV
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['t', 'ecg'])  # Write header
    for time, ecg in zip(t, ecg_values):
        writer.writerow([time, ecg])

print(f"ECG signal data written to {csv_file_path}")

