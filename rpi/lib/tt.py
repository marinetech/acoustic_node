import serial, time, array, binascii


ser = serial.Serial()
ser.port = "/dev/ttyUSB1"
ser.baudrate = 38400
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.timeout = 1
ser.xonxoff = False
ser.rtscts = False
ser.dsrdtr = False
ser.open()
ser.flushInput()
ser.flushOutput()

a0 = array.array('B',[0xA5,0x69,0x03,0x10,0xEC]) # READ PARAMS
a1 = array.array('B',[0xA5,0x69,0x03,0x60,0x9c]) # READ I&V
a2 = array.array('B',[0xA5,0x69,0x03,0x61,0x9b]) # READ ACTUAL AH

ser.write(a0)
r0 = binascii.hexlify(ser.read(25))
ah = (int(r0[6:8] + r0[4:6] + r0[2:4] + r0[0:2],16)/1000)/3600.0
Vbat = int(r0[10:12] + r0[8:10],16)
I_Factor = int(r0[14:16]+ r0[12:14],16)
I_Offset = int(r0[18:20]+ r0[16:18],16)

ser.write(a1)
r1 = binascii.hexlify(ser.read(25))
Current = int(r1[2:4]+r1[0:2],16)
CurrentCurrent = ((I_Offset - Current)*I_Factor)/10000
Volt = int(r1[6:8]+r1[4:6],16)
VoltVal = (Volt*Vbat)/10000

CurrentCurrent = CurrentCurrent if CurrentCurrent > 0 else CurrentCurrent*-1

ser.write(a2)
r2 = binascii.hexlify(ser.read(25))

AH_low = int(r2[2:4]+r2[0:2],16)
AH_high = int(r2[6:8]+r2[4:6],16)

print ("Design Ampere hour : " + str(ah))
print ("Current : " + str(CurrentCurrent))
print ("Volt : " + str(VoltVal))
print ("Amp /s : " + str(AH_low))
print ("% capacity : " + str(AH_high / ah) + "%")
