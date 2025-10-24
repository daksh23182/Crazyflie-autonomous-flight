import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# --- Load logged trajectory ---
df = pd.read_csv("trajectory_log.csv")

# Convert timestamp if available
if 'Timestamp' in df.columns:
    try:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    except:
        pass

# --- Expected trajectory (ideal path) ---
expected_points = [
    (2.50, 3.3, 0.0),
    (2.50, 3.3, 1.0),
    (2.50, 3.3, 1.0),
    (1.25, 3.3, 1.0),
    (1.25, 3.3, 0.0),
    (1.25, 3.3, 1.0),
    (2.20, 3.3, 1.0),
    (2.20, 3.3, 0.0)
]
x_exp, y_exp, z_exp = zip(*expected_points)

# --- 3D plot comparing both ---
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Logged trajectory
ax.plot(df['X'], df['Y'], df['Z'], label='Logged Trajectory', color='blue', linewidth=2)

# Expected trajectory
ax.plot(x_exp, y_exp, z_exp, 'ro--', label='Expected Path', linewidth=2)

# --- Equal scale on all axes ---
all_x = np.concatenate([df['X'].values, x_exp])
all_y = np.concatenate([df['Y'].values, y_exp])
all_z = np.concatenate([df['Z'].values, z_exp])

min_val = min(all_x.min(), all_y.min(), all_z.min())
max_val = max(all_x.max(), all_y.max(), all_z.max())

# Add a small margin
margin = (max_val - min_val) * 0.05
ax.set_xlim(min_val - margin, max_val + margin)
ax.set_ylim(min_val - margin, max_val + margin)
ax.set_zlim(min_val - margin, max_val + margin)

ax.set_box_aspect([1, 1, 1])  # Keep all axes proportional

# --- Labels and title ---
ax.set_title("Crazyflie Flight Trajectory (Expected vs Logged)")
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_zlabel('Z (m)')
ax.legend()
ax.grid(True)

plt.show()
