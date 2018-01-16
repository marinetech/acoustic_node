# import datetime
from lib.network import *
from lib.log import *
from lib.gpio import *
from lib.sdm import *
from conf.main_cfg import *


if  __name__ == "__main__":
    print("")
    print("*** Starting the main loop of the acoustic-node operation ***")
    print("")
    try:
        log = Log(log_path)
        net = Network(net_protocol, log)
        gpio = CtrlGPIO(log)
        sdm = SDM(modem_ip, modem_port, rpi_tasks, rpi_bin, log)
    except Exception as e:
        print("-E- " + str(e))
        exit(1)


    gpio.set_comm_mode() # pwr-on rpi + dsl
    net.connect_func(pc104_ip,pc104_user,pc104_user_passwd) # establish ssh connection with pc104
    net.get_func(pc104_tasks , rpi_tasks) # get new tasks
    gpio.set_operation_mode # pwr-on rpi + modem
    sdm.process_tasks() # run SDM tasks
    gpio.set_comm_mode() # pwr-on rpi + dsl
    net.put_func(rpi_done_folder, pc104_done_folder) # upload results
