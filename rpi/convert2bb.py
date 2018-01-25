# import matplotlib.pyplot as plt
# plt.plot([1,2,3,4])
# plt.ylabel('some numbers')
# plt.show()


import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import scipy.io

def convert(Signal, Fcarrier, Fs, Factor, FiltCoeff, FiltMem=None, Phase=None):

    if Phase is None:
        Phase = 0

    if FiltMem is None:
        FiltMem = numpy.zeros(len(FiltCoeff)-1)

    DataLen =  len(Signal); # The signal length.

    # time = 0:1/Fs:(DataLen-1)/Fs # Time vector.
    time = numpy.arange(0, (DataLen-1)/Fs, 1/Fs)

    # Calculate the NextPhase.
    NextPhase = (time[-1] + 1/Fs ) * 2 * math.pi * Fcarrier + Phase
    NextPhase = round(NextPhase,1)
    m1 = round(2*math.pi,4)
    NextPhase  = matlab_mod(NextPhase, m1)

    SignalBB = numpy.exp (-1j * (2 * math.pi * Fcarrier * time + Phase))
    SignalBB, _ = scipy.signal.lfilter(FiltCoeff, 1, SignalBB, -1 ,FiltMem)
    SignalBB1 = SignalBB[0:-1:Factor]
    SignalBB2 = numpy.round(SignalBB1, 4)

    outstr = ""
    for f in SignalBB2:
        s = str(f).replace("(", "").replace(")", "").replace("j", "i")
        outstr = outstr+s+","

    hOut = open("Output.txt", "w")
    hOut.write(outstr[:-1])
    hOut.close()

Ref = scipy.io.loadmat('/home/ilan/projects/Experiments/bb_test/OneLFMSignal.mat')


# Fs = 96e3
# Ts = 0.1
# f0 = 7e3
# f1 = 17e3
# Fc = (f0+f1)/2
# W = f1 - f0
#
# t=np.linspace(0,Ts,num=Ts*Fs,endpoint=True,retstep=True)
# tt=t[0]
#
# L = 128  # BP filter length
# #BPF:
# B = 1.2*W # BPF band
#
# #BB conversion:
#
# bLPF = signal.firwin(L+1,B/Fs,window='hamming')
# Factor = 5
# FsBB = Fs/Factor;
#
# Ref=signal.chirp(tt,f0,tt[-1],f1,method='linear')
#
# DataLen=len(Ref) #The signal length
# time=np.arange(0,((DataLen-1)/Fs)+(1/Fs),1/Fs,dtype='float64')#observation time T [s]
#
# #Calculate the NextPhase.
# FiltMem = np.zeros((1,len(bLPF)-1))
# FiltMem = FiltMem.reshape((-1,))
# Factor = 5
#
# Phase=0
# NextPhase=(time[-1] + 1/Fs ) * 2 * np.pi * Fc + Phase
# NextPhase=np.mod(NextPhase,2*np.pi)
# SignalBB = Ref*(np.e**(-1j*(2 * np.pi * Fc * time + Phase))) #Shift the signal to BaseBand
#
#
# plt.figure(1)
# plt.subplot(411)
# plt.plot(tt,Ref)
# plt.title('Original Signal')
# plt.subplot(412)
# plt.plot(tt,np.real(SignalBB))
# plt.title('The signal Shifted to baseband')
#
#
#
# SignalBB2, FiltMem2 = signal.lfilter(bLPF,1,SignalBB,zi=FiltMem)
#
# plt.subplot(413)
# plt.plot(tt,np.real(SignalBB2))
# plt.title('The signal after filter')
#
# SignalBB3 = SignalBB2[0:-1:Factor]
# FiltMemDec = FiltMem2[1:-1:Factor] # Decimation.
# FiltMem2 = np.reshape(FiltMem2,(1,-1))       # Convert to row vector
# FiltMemDec = np.reshape(FiltMemDec,(1,-1))   # Convert to row vector
#
# plt.subplot(414)
# plt.plot(tt[1:-1:Factor],np.real(SignalBB3))
# plt.title('Decimated signal')
