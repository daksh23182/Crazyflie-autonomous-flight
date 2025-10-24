import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- Load logged trajectory ---
df = pd.read_csv("trajectory_log.csv")

# Normalize column names
df.columns = [c.strip().lower() for c in df.columns]

# Compute relative time (seconds)
if 'timestamp' in df.columns:
    t0 = df['timestamp'].iloc[0]
    df['time_sec'] = (df['timestamp'] - t0) / 1000.0  # assuming timestamp is in ms
else:
    df['time_sec'] = np.arange(len(df)) * 0.1  # assume 100 ms interval

# --- Define expected waypoints ---
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

# Create evenly spaced expected times matching your flight duration
expected_time = np.linspace(0, df['time_sec'].max(), len(expected_points))
x_exp, y_exp, z_exp = zip(*expected_points)

# --- Determine common Y-axis scale for X, Y, Z plots ---
min_val = min(df['x'].min(), df['y'].min(), df['z'].min(),
              min(x_exp), min(y_exp), min(z_exp))
max_val = max(df['x'].max(), df['y'].max(), df['z'].max(),
              max(x_exp), max(y_exp), max(z_exp))

# Add a small margin for visual clarity
margin = (max_val - min_val) * 0.05
ymin, ymax = min_val - margin, max_val + margin

# --- Plot Timestamp vs X, Y, Z ---
plt.figure(figsize=(12, 9))

# X vs Time
plt.subplot(3, 1, 1)
plt.plot(df['time_sec'], df['x'], label='Logged X', color='blue')
plt.plot(expected_time, x_exp, 'r--', label='Expected X')
plt.scatter(expected_time, x_exp, color='red', s=50, zorder=5, label='Waypoints')
plt.title("Timestamp vs X")
plt.xlabel("Time (s)")
plt.ylabel("X (m)")
plt.legend()
plt.grid(True)
plt.ylim(ymin, ymax)

# Y vs Time
plt.subplot(3, 1, 2)
plt.plot(df['time_sec'], df['y'], label='Logged Y', color='green')
plt.plot(expected_time, y_exp, 'r--', label='Expected Y')
plt.scatter(expected_time, y_exp, color='red', s=50, zorder=5, label='Waypoints')
plt.title("Timestamp vs Y")
plt.xlabel("Time (s)")
plt.ylabel("Y (m)")
plt.legend()
plt.grid(True)
plt.ylim(ymin, ymax)

# Z vs Time
plt.subplot(3, 1, 3)
plt.plot(df['time_sec'], df['z'], label='Logged Z', color='purple')
plt.plot(expected_time, z_exp, 'r--', label='Expected Z')
plt.scatter(expected_time, z_exp, color='red', s=50, zorder=5, label='Waypoints')
plt.title("Timestamp vs Z")
plt.xlabel("Time (s)")
plt.ylabel("Z (m)")
plt.legend()
plt.grid(True)
plt.ylim(ymin, ymax)

plt.tight_layout()
plt.show()
