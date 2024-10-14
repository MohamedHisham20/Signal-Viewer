import numpy as np
import pandas as pd


# Generate data
x = np.linspace(0, 2 * np.pi, 100)  # 100 points from 0 to 2*pi
y = np.cos(x)

# Create a DataFrame
data = pd.DataFrame({'x': x, 'y': y})

# Save to CSV
data.to_csv('cos_wave.csv', index=False)

