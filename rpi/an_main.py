# import datetime
from lib.network import *
from lib.log import *
from lib.gpio import *
from lib.sdm import *
from conf.main_cfg import *
import os


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



    #produce battery level log.
    # gpio.set_all_on() # pwr-on rpi + dsl
    # try:
    #     log.print_log("-I- attempting to produce battery level")
    #     import get_battery_level
    # except Exception as e:
    #     log.print_log("-E- faliled to read battery data")
    #     log.print_log(e)

    # execute the main cycle
    gpio.set_comm_mode() # pwr-on rpi + dsl
    net.connect_func(pc104_ip,pc104_user,pc104_user_passwd) # establish ssh connection with pc104
    net.get_func(pc104_tasks , rpi_tasks) # get new tasks
    gpio.set_operation_mode() # pwr-on rpi + modem
    sdm.process_tasks() # run SDM tasks
    gpio.set_comm_mode() # pwr-on rpi + dsl
    net.put_func(rpi_done, pc104_done) # upload results
    gpio.set_process_mode() # rpi only
    gpio.set_all_on()
