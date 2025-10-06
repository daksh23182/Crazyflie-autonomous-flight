import logging
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger


# Change this to match your Crazyflie
URI = 'radio://0/80/2M/E7E7E7E7E7'


# ---------------- Step 1: Connection ----------------
def simple_connect():
    print("\n[Step 1] Connection test")
    print("Yeah, I'm connected! :D")
    time.sleep(2)
    print("Now I will disconnect :'(")


# ---------------- Step 2: Logging ----------------
def log_stab_callback(timestamp, data, logconf):
    print('[%d][%s]: %s' % (timestamp, logconf.name, data))


def simple_log_async(scf):
    print("\n[Step 2] Logging test (5 seconds)")
    lg_stab = LogConfig(name='Stabilizer', period_in_ms=100)
    lg_stab.add_variable('stabilizer.roll', 'float')
    lg_stab.add_variable('stabilizer.pitch', 'float')
    lg_stab.add_variable('stabilizer.yaw', 'float')

    cf = scf.cf
    cf.log.add_config(lg_stab)
    lg_stab.data_received_cb.add_callback(log_stab_callback)

    lg_stab.start()
    time.sleep(5)   # log for 5 seconds
    lg_stab.stop()


# ---------------- Step 3: Parameters ----------------
def param_stab_est_callback(name, value):
    print('Parameter update -> %s = %s' % (name, value))


def simple_param_async(scf):
    print("\n[Step 3] Parameter test")
    cf = scf.cf

    group = 'stabilizer'
    name = 'estimator'
    full_name = group + '.' + name

    cf.param.add_update_callback(group=group, name=name,
                                 cb=param_stab_est_callback)

    time.sleep(1)
    print("Setting estimator = 2")
    cf.param.set_value(full_name, 2)   # change
    time.sleep(1)

    print("Restoring estimator = 1")
    cf.param.set_value(full_name, 1)   # restore
    time.sleep(1)


# ---------------- Main ----------------
if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers(enable_debug_driver=False)

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        simple_connect()
        simple_log_async(scf)
        simple_param_async(scf)

    print("\n✅ Tutorial 1 complete! All tests done.")
