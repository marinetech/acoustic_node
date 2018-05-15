import datetime
from lib.network import *
from lib.log import *
from lib.gpio import *
from lib.sdm import *
from conf.main_cfg import *
import os
from shutil import copyfile
import time


def set_wdir():
    wdir = (os.path.dirname(os.path.realpath(__file__)))
    print("wdir: " + wdir)
    os.chdir(wdir)


if  __name__ == "__main__":
    print("")
    print("*** Starting the main loop of the acoustic-node operation ***")
    print("")
    try:
        set_wdir()
        log = Log(log_path)
        net = Network(net_protocol, log)
        gpio = CtrlGPIO(log)
        sdm = SDM(rpi_tasks, rpi_done, log)
    except Exception as e:
        print("-E- " + str(e))
        exit(1)

    # Clean procedure
    log.print_log("-I- cleanning relevant areas")
    for dir in [rpi_done, rpi_tasks]:
        for f in os.listdir(dir):
            os.remove(dir + "/" + f)

    # produce battery level log.
    try:
        log.print_log("-I- attempting to produce battery level")
        import get_battery_level
        get_battery_level.execute(rpi_done, "/dev/ttyUSB1") #arg1 - the location of output log; arg2 - which serial port we use
    except Exception as e:
        log.print_log("-E- Failed to read battery data")
        log.print_log(str(e))

    # execute the main cycle
    time.sleep(120)
    net.connect_func(pc104_ip,pc104_user,pc104_user_passwd) # establish ssh connection with pc104
    net.get_func(pc104_tasks , rpi_tasks) # get new tasks

    # check if there is IMU tasks
    imu_conf = rpi_tasks + "/imu.json"
    if os.path.isfile(imu_conf):
        ### produce IMU log.
        try:
            log.print_log("-I- attempting to produce IMU info")
            from lib.get_imu_info import *
            imu_main(rpi_done, imu_conf)
            os.remove(imu_conf)
        except Exception as e:
            log.print_log("-E- Failed to read imu data")
            log.print_log(str(e))


    try:
        sdm.process_tasks() # run SDM tasks
    except Exception as e:
        log.print_log("-E- Failed to process tasks")
        log.print_log(str(e))

    # copy the main log to the upload dir.
    try:
        copyfile(log_path,  rpi_done + "/" + os.path.basename(log_path))
    except Exception as e:
        log.print_log("-E- Failed to copy log to upload dir")
        log.print_log(str(e))

    # gpio.set_comm_mode() # pwr-on rpi + dsl (turn-off modem)
    log.print_log("-I- uploading results")
    net.put_func(rpi_done, pc104_done) # upload results
    log.print_log("-I- done")
    os.remove(log_path)
    # gpio.set_process_mode() # rpi only
    # gpio.set_all_on()


    ########### NEED TO COPY LOG TO RPI_DONE
