import time
import logging
import csv
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.log import LogConfig

# Enable high-level commander
from cflib.crazyflie.high_level_commander import HighLevelCommander

# URI: replace with your drone's address
uri = 'radio://0/80/2M/E7E7E7E7E7'

# Set logging level to ERROR to keep the console clean
logging.basicConfig(level=logging.ERROR)

# A list to store the logged position data
trajectory_log = []

def log_pos_callback(timestamp, data, logconf):
    """
    Callback function that is called when new log data is received.
    It appends the current position estimate to the trajectory_log list.
    """
    global trajectory_log
    pos_x = data.get('stateEstimate.x', 0.0)
    pos_y = data.get('stateEstimate.y', 0.0)
    pos_z = data.get('stateEstimate.z', 0.0)
    trajectory_log.append((timestamp, pos_x, pos_y, pos_z))
    print(f"Timestamp: {timestamp} | Position: x={pos_x:.3f}, y={pos_y:.3f}, z={pos_z:.3f}")

def write_log_to_csv(filename="trajectory_log.csv"):
    """Writes the collected trajectory data to a CSV file."""
    if not trajectory_log:
        print("No trajectory data was logged.")
        return

    with open(filename, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        # Write the header row
        writer.writerow(['Timestamp', 'X', 'Y', 'Z'])
        # Write all the data rows
        writer.writerows(trajectory_log)
    print(f"\nTrajectory data has been successfully saved to '{filename}'")


if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    # Create a LogConfig object for position logging
    log_conf = LogConfig(name='PositionLog', period_in_ms=100)
    log_conf.add_variable('stateEstimate.x', 'float')
    log_conf.add_variable('stateEstimate.y', 'float')
    log_conf.add_variable('stateEstimate.z', 'float')

    # Use SyncCrazyflie for a synchronous connection
    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
        hlc = scf.cf.high_level_commander
        cf = scf.cf

        # Add the log configuration and set the callback
        cf.log.add_config(log_conf)
        log_conf.data_received_cb.add_callback(log_pos_callback)

        try:
            # Start logging
            log_conf.start()
            print("Logging started.")

            # --- FLIGHT PLAN ---
            print("Taking off to 1.5 m...")
            hlc.takeoff(1.5, 4.0)
            time.sleep(5)

            print("Moving to first waypoint...")
            hlc.go_to(2.23, 3.26, 1.50, 0.0, 6.0)
            time.sleep(6)

            print("Moving to second waypoint...")
            hlc.go_to(0.57, 3.0, 1.50, 0.0, 6.0)
            time.sleep(6)

            print("First landing...")
            hlc.land(0.0, 8.0)
            time.sleep(6)

            print("Second takeoff...")
            hlc.takeoff(1.5, 4.0)
            time.sleep(5)

            print("Returning to first waypoint...")
            hlc.go_to(2.23, 3.26, 1.5, 0.0, 6.0)
            time.sleep(5)

            print("Final landing...")
            hlc.land(0.0, 6.0)
            time.sleep(6)

        finally:
            # Stop logging before the connection is closed
            log_conf.stop()
            print("\nLogging stopped.")
            
            # Note: hlc.stop() is not a valid command.
            # The motors stop automatically after landing.

    # After the 'with' block, the connection is closed.
    # Now, write the collected log data to a file.
    write_log_to_csv()
    
    print("Done!")