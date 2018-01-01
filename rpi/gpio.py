import time
import RPi.GPIO as GPIO


class CtrlGPIO:

	def __init__(self):
		# to use Raspberry Pi board pin numbers
		GPIO.setmode(GPIO.BCM)
		# disable 'channel is already in use' warnings
		GPIO.setwarnings(False)
		# GPIO Map
		self.dsl_io = 10
		self.modem_io = 22
		self.battery_io = 27
		self.notinuse_io = 9
		# set up the GPIO channels - all outputs
		GPIO.setup(27, GPIO.OUT)
		GPIO.setup(22, GPIO.OUT)
		GPIO.setup(10, GPIO.OUT)
		GPIO.setup(9, GPIO.OUT)
		GPIO.output(self.notinuse_io, GPIO.HIGH)

	def set_process_mode(self):
		GPIO.output(self.dsl_io, GPIO.HIGH)
		GPIO.output(self.modem_io, GPIO.HIGH)
		GPIO.output(self.battery_io, GPIO.HIGH)

	def set_comm_mode(self):
		GPIO.output(self.battery_io, GPIO.LOW)
		GPIO.output(self.dsl_io, GPIO.LOW)
		GPIO.output(self.modem_io, GPIO.HIGH)

	def set_operation_mode(self):
		GPIO.output(self.battery_io, GPIO.LOW)
		GPIO.output(self.dsl_io, GPIO.HIGH)
		GPIO.output(self.modem_io, GPIO.LOW)

	def cleanup(self):
		GPIO.cleanup()


if  __name__ == "__main__":
	ioctrl = CtrlGPIO()
	for mode in ["set_process_mode", "set_comm_mode", "set_operation_mode"]:
		print(mode)
		getattr(ioctrl, mode)()
		time.sleep(20)
	ioctrl.cleanup()
