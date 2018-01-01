import datetime

# general
now = datetime.datetime.now().strftime("%Y%m%d%H%M")
net_protocol = "ssh"

# pc104 related settings
pc104_ip = "127.0.0.1"
pc104_tasks_folder = "/home/ilan/projects/acoustic_node/pc104_tasks"
pc104_done_folder = "/home/ilan/projects/acoustic_node/pc104_done"
pc104_user = "pi"
pc104_user_passwd = "raspberry"


# rpi file system
rpi_tasks_folder = "/home/ilan/projects/acoustic_node/rpi_tasks"
rpi_done_folder = "/home/ilan/projects/acoustic_node/rpi_done"
rpi_logs = "/home/ilan/projects/acoustic_node/rpi/logs"
log_path = rpi_logs + "/wakeup_" + now + ".log"



# rpi-gpio realated settings
