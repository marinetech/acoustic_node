import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import scipy.io
from scipy import signal
sys.path.append("../rpi/lib")
import matlab

if __name__ == "__main__":

    # ------------------------------------------------------------------------------
    # The following test implements the entire detection flow.
    # convert TxRef to TxRef_BB
    # Foreach Rx file:
    #   convert the signal to RxSig_BB
    #   mf = MF(TxRef_BB, RxSig_BB)
    #   Foreach element in mf:
    #       if element > threshold:
    #           Found detection!
    #           save Rx_BB
    # ------------------------------------------------------------------------------


    # thershold = 1
    # Fc = 12000.0
    # Fs = 62500.0
    # Factor = 2
    # matlab_ref = scipy.io.loadmat('../resources/RefForTankTest.mat')
    # TxRef = matlab.loadSignalFromFile("../resources/TxRef")

    matlab_ref = matlab.load_mat('/home/ilan/projects/Experiments/Eilat/mat/ParamForSigLowNarrow.mat')
    if matlab_ref is None:
        exit()

    thershold = matlab_ref['thershold']
    Fc = float(matlab_ref['Fc'])
    Fs = float(matlab_ref['Fs'])
    Factor = int(matlab_ref['Factor'])
    bLPF = matlab_ref['bLPF'].reshape((-1,))
    TxRef = matlab_ref['TxRef'].reshape((-1,))
    TxRef_BB = matlab.convert2bb(TxRef, Fc, Fs, Factor, bLPF)

    # Read & analyze Rx files
    rx_dir = "/home/ilan/projects/Experiments/test/tmp"
    for f in os.listdir(rx_dir):
        RxSig = matlab.loadSignalFromFile(rx_dir + "/" + f)
        RxSig = matlab.pre_bb_norm(RxSig)
        np.savetxt(rx_dir + "/" + f + ".prebb", RxSig)
        RxSig_BB = matlab.convert2bb(RxSig, float(Fc), float(Fs), int(Factor), bLPF)
        np.savetxt(rx_dir + "/" + f + ".afterbb", RxSig)
        mf = matlab.normCorrC(TxRef_BB, RxSig_BB)
        np.savetxt(rx_dir + "/" + f + ".aftermf", RxSig)
        if matlab.has_detection(mf, thershold):
            print("detected: " + f)
