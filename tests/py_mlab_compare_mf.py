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
    # The following test should validate matlab.normCorrC (aka Lisa's function):
    #   it runs matlab.normCorrC on BaseBanded signal
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
    mf_ref = matlab_ref['RefBB'].reshape((-1,))
    lisa_mf = matlab.normCorrC(mf_ref, yuri_bb)

    print("Lisa's returned vector:")
    print(type(lisa_mf))
    print(lisa_mf.shape)
    print()

    # # Read & analyze Rx files
    # rx_dir = "/home/ilan/projects/Experiments/bb_test/tmp"
    # for f in os.listdir(rx_dir):
    #     vec = matlab.loadSignalFromFile(rx_dir + "/" + f)
    #     print(type(vec))
    #     print(vec.shape)
    #     print()


    plt.figure(1)
    plt.subplot(411)
    plt.plot(lisa_mf)
    plt.title("Lisa's MF")
    plt.show()
