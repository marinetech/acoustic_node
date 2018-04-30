import time
import RPi.GPIO as GPIO



class CtrlGPIO:

	def __init__(self, log):
		# to use Raspberry Pi board pin numbers
		GPIO.setmode(GPIO.BCM)
		# disable 'channel is already in use' warnings
		GPIO.setwarnings(False)
		# GPIO Map
		self.dsl_io = 10
		self.modem_io = 22 #K2
		self.battery_io = 27
		self.notinuse_io = 9
		# set up the GPIO channels - all outputs
		GPIO.setup(27, GPIO.OUT)
		GPIO.setup(22, GPIO.OUT)
		GPIO.setup(10, GPIO.OUT)
		GPIO.setup(9, GPIO.OUT)
		GPIO.output(self.notinuse_io, GPIO.HIGH)

		self.log = log
		self.log.print_log("-I- GPIO obj was Initialized successfully")

	# rpi is on, all the rest is off.
	# used when rpi has no need to cmmunicate with pc104 or with modem
	def set_process_mode(self):
		self.log.print_log("-I- GPIO: setting process mode")
		GPIO.output(self.dsl_io, GPIO.HIGH)
		GPIO.output(self.modem_io, GPIO.HIGH)
		GPIO.output(self.battery_io, GPIO.HIGH)
		time.sleep(5)

	# rpi, battery, dsl are on, modem is off
	# used when rpi has to communicate with pc104
	def set_comm_mode(self):
		self.log.print_log("-I- GPIO: setting communication mode")
		GPIO.output(self.battery_io, GPIO.LOW)
		GPIO.output(self.dsl_io, GPIO.LOW)
		GPIO.output(self.modem_io, GPIO.HIGH)
		time.sleep(5)

	# rpi, battery, modem are on, dsl is off
	# used when rpi has to communicate with modem
	def set_operation_mode(self):
		self.log.print_log("-I- GPIO: setting operation mode")
		GPIO.output(self.battery_io, GPIO.LOW)
		GPIO.output(self.dsl_io, GPIO.HIGH)
		GPIO.output(self.modem_io, GPIO.LOW)
		time.sleep(5) #let the modem to come up

	def set_all_on(self):
		self.log.print_log("-I- GPIO: setting all-one mode")
		GPIO.output(self.battery_io, GPIO.LOW)
		GPIO.output(self.dsl_io, GPIO.LOW)
		GPIO.output(self.modem_io, GPIO.LOW)
		time.sleep(5)


	def cleanup(self):
		GPIO.cleanup()


if  __name__ == "__main__":
	from log import *
	log = Log("./gpio.log")

	ioctrl = CtrlGPIO(log)
	# for mode in ["set_process_mode", "set_comm_mode", "set_operation_mode", "set_all_on"]:
	# 	print(mode)
	# 	getattr(ioctrl, mode)()
	# 	time.sleep(1)
	# exit()
	# ioctrl.cleanup()
	ioctrl.set_all_on()
