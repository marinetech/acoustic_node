import datetime

# general
now = datetime.datetime.now().strftime("%Y%m%d%H%M")
net_protocol = "ssh"

# pc104 related settings
pc104_ip = "192.168.88.15"
pc104_tasks = "/home/acoustic_node/tasks"
pc104_done = "/home/acoustic_node/done"
pc104_user = "acoustic_node"
pc104_user_passwd = "tabsbuoy"


# rpi file system
rpi_root = "/home/pi/acoustic_node"
#rpi_root = "/home/ilan/projects/acoustic_node/rpi"
# rpi_root = "/home/ilan/projects/acoustic_node" #testing env
rpi_tasks = rpi_root + "/tasks"
rpi_done = rpi_root + "/done"
rpi_logs = rpi_root + "/logs"
rpi_bin = rpi_root + "/bin"
log_path = rpi_logs + "/an_main_" + now + ".log"


# modem related settings
modem_ip = "192.168.88.138"
modem_port = "9200"
