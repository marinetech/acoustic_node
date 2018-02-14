import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import scipy.io
from scipy import signal
sys.path.append("../rpi/lib")
import matlab

if __name__ == "__main__":

    #   ------------------------------------------------------------------------------
    # The following test should validate matlab.convert2bb (aka Yuri's function):
    #   it runs matlab.convert2bb on a set of predefined parameters
    #   it compares the results to the original matlab results
    #   predefined parameters & matlab results are both taken from mat reference file.
    #   ------------------------------------------------------------------------------

    # predefined signal and parameters
    matlab_ref = scipy.io.loadmat('../resources/RefForTankTest.mat')
    Ref = matlab_ref['OneLFMSignal'].reshape((-1,))
    Fc = 12000.0
    Fs = 62500.0
    Factor = 2
    bLPF = matlab_ref['bLPF'].reshape((-1,))

    yuri_bb = matlab.convert2bb(Ref, Fc, Fs, Factor, bLPF)

    print("Yuri's returned vector:")
    print(type(yuri_bb))
    print(yuri_bb.shape)
    print()

    roee_bb = matlab_ref['RefBB'].reshape((-1,))
    print("Roee's original results")
    print(type(roee_bb))
    print(roee_bb.shape)
    print()

    print("Values are similiar (True/False): " + str(np.allclose(yuri_bb,roee_bb)))
    print()

    plt.figure(1)
    plt.subplot(411)
    plt.plot(np.real(yuri_bb))
    plt.title("Yuri's BB")


    plt.subplot(413)
    plt.plot(np.real(roee_bb))
    plt.title("Roee's BB")
    plt.show()

    
