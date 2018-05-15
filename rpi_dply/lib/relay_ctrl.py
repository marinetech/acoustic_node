# Not part of the project - used for debug only !!!

# import gpio
import sys

usage = "Usage:\n\tpython3 " + sys.argv[0] + " <io> <on|off>"

if len(sys.argv) != 3:
    print(usage)
    exit()

# ioctrl = CtrlGPIO("relay.log")
# ioctrl.switch_io(10, True)
