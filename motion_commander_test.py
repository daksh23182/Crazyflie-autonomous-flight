import time
import logging
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

# Enable high-level commander
from cflib.crazyflie.high_level_commander import HighLevelCommander

# URI: replace with the one from `python3 -m cflib.crtp`
uri = 'radio://0/80/2M/E7E7E7E7E7'

logging.basicConfig(level=logging.ERROR)

if __name__ == '__main__':
    # Initialize driversf
    cflib.crtp.init_drivers()

    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
        hlc = scf.cf.high_level_commander

        print("Taking off to 1.5 m...")
        hlc.takeoff(1.5, 4.0)  
        time.sleep(5)

      
        hlc.go_to(2.23,3.26,1.50 ,0.0,6.0)  # stay at 
        time.sleep(6)  # keep hovering

        hlc.go_to(0.57,3,1.50 ,0.0,6.0)  # stay at 
        time.sleep(6)  # keep hovering
    
        hlc.land(0.00, 8.0)
        time.sleep(6)
    
        hlc.takeoff(1.5, 4.0)  
        time.sleep(5)

        hlc.go_to(2.23, 3.26,1.5 ,0.0,6.0)  # stay at 
        time.sleep(5)  # keep hovering
        print("Landing...")
        hlc.land(0.00, 6.0)
        time.sleep(6)
        hlc.stop()
        print("Done!")
