# import datetime
from network import *
from log import *
from main_cfg import *


if  __name__ == "__main__":
    log = Log(log_path)

    try:
        net = Network(net_protocol)
    except Exception as e:
        self.log.print_log("-E- " + e)
        exit(1)

    net.connect_func(pc104_ip,pc104_user,pc104_user_passwd)
    net.get_func(pc104_tasks_folder , rpi_tasks_folder)
    net.put_func(rpi_done_folder, pc104_done_folder)
