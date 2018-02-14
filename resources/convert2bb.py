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
        FiltMem = np.zeros((1, len(FiltCoeff)-1))
        FiltMem = FiltMem.reshape((-1,))

    DataLen =  len(Signal); # Signal's length.
    # time = np.arange(0,((DataLen-1)/Fs)+(1/Fs),1/Fs)  #observation time T [s]
    # print("len.time: " + str(len(time)))
    # time = np.arange(0,((DataLen-1)/Fs),1/Fs)  #observation time T [s]
    #
    time = np.linspace(0, (DataLen-1)/Fs, DataLen)


    # Calculate the NextPhase.
    NextPhase = (time[-1] + 1/Fs ) * 2 * np.pi * Fcarrier + Phase
    NextPhase = np.mod(NextPhase, 2 * np.pi)

    signal_after_baseband = Signal * (np.e** (-1j * (2 * np.pi * Fc * time + Phase))) #Shift the signal to BaseBand
    signal_after_filter, FiltMem2 = scipy.signal.lfilter(FiltCoeff, 1, signal_after_baseband, zi=FiltMem)
    signal_after_decimation = signal_after_filter[0::Factor]

    FiltMemDec = FiltMem2[1:-1:Factor]
    FiltMem2 = np.reshape(FiltMem2,(1,-1))       # Convert to row vector
    FiltMemDec = np.reshape(FiltMemDec,(1,-1))   # Convert to row vector

    return signal_after_decimation


#------ Main Body - checks convert function --------#
if __name__ == "__main__":
    # Fs = 96e3
    # Ts = 0.1
    # f0 = 7e3
    # f1 = 17e3
    # Fc = (f0+f1)/2
    # W = f1 - f0
    # t = np.linspace(0, Ts, Ts*Fs)
    # L = 128;  # BP filter length
    # B = 1.2*W   # BPF band
    # # bLPF = scipy.signal.firwin(L, B/Fs);
    # bLPF = signal.firwin(L+1,B/Fs,window='hamming')
    # Factor = 5;
    # # FsBB = Fs/Factor;
    # #
    # #Ref = chirp(t,f0,t(end),f1);
    # Ref = scipy.signal.chirp(t,f0, t[-1], f1)
    # # # [RefBB, ~, ~, ~] = ConvertToBBVer0(Ref, Fc, Fs, Factor, bLPF);
    # #
    # # # print("Fs = "  + str(Fs))
    # # # # print("Ts = "  + str(Ts))
    # # # # print("f0 = "  + str(f0))
    # # # # print("f1 = "  + str(f1))
    # # # print("Fc = "  + str(Fc))
    # # # print("W = "  + str(W))
    # # # print("t = "  + str(t))
    # # print("Ref = "  + str(type(Ref)))
    # # print("Ref = "  + str(Ref.shape))
    # # print("Ref = "  + str(Ref))
    # # # print("bLPF = "  + str(bLPF.shape))
    # # # print("Factor = "  + str(Factor))
    # #
    # # # convert(Ref, Fc, Fs, Factor, bLPF)

    matlab_ref = scipy.io.loadmat('/home/ilan/projects/Experiments/bb_test/RefForTankTest.mat')

    Ref = matlab_ref['OneLFMSignal'].reshape((-1,))
    Fc = 12000.0
    Fs = 62500.0
    Factor = 2
    bLPF = matlab_ref['bLPF'].reshape((-1,))
    yuri_bb = convert(Ref, Fc, Fs, Factor, bLPF)


    # t = scipy.io.whosmat('/home/ilan/projects/Experiments/bb_test/OneLFMSignal.mat')
    print("yuri_bb")
    print(type(yuri_bb))
    print(yuri_bb.shape)



    roee_bb = matlab_ref['RefBB'].reshape((-1,))
    print("roee_bb")
    print(type(roee_bb))
    print(roee_bb.shape)
    # print("last: " + str(roee_bb[-1]))

    print("allclose? " + str(np.allclose(yuri_bb,roee_bb)))

    plt.figure(1)
    plt.subplot(411)
    plt.plot(np.real(yuri_bb))
    plt.title('Yuri BB')


    plt.subplot(412)
    plt.plot(np.real(roee_bb))
    plt.title('Roee BB')
    plt.show()
