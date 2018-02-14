import numpy as np
from scipy import signal
import scipy.io
import os.path


def convert2bb(Signal, Fcarrier, Fs, Factor, FiltCoeff, FiltMem=None, Phase=0):
    # convert to baseband - this a translation of matlab code (written by Roee Diamant)
    # The function returns the converted Signal(1st argument)
    # ----------------------------------------------------------------------------------

    # set default FiltMem
    if FiltMem is None:
        FiltMem = np.zeros((1, len(FiltCoeff)-1))
        FiltMem = FiltMem.reshape((-1,))

    DataLen =  len(Signal); # Signal's length.
    time = np.linspace(0, (DataLen-1)/Fs, DataLen) #linspace(start, stop, num_of_smaples)

    # Calculate the NextPhase.
    NextPhase = (time[-1] + 1/Fs ) * 2 * np.pi * Fcarrier + Phase
    NextPhase = np.mod(NextPhase, 2 * np.pi)

    signal_after_baseband = Signal * (np.e** (-1j * (2 * np.pi * Fcarrier * time + Phase))) #Shift the signal to BaseBand
    signal_after_filter, FiltMem2 = scipy.signal.lfilter(FiltCoeff, 1, signal_after_baseband, zi=FiltMem) #low pass filter
    signal_after_decimation = signal_after_filter[0::Factor] # and decimation.

    FiltMemDec = FiltMem2[1:-1:Factor]
    FiltMem2 = np.reshape(FiltMem2,(1,-1))       # Convert to row vector
    FiltMemDec = np.reshape(FiltMemDec,(1,-1))   # Convert to row vector

    return signal_after_decimation


def turnToVector(vec):
    return vec.flatten(), np.size(vec.flatten())


def normCorrC(ref, sig, short=1, useC=1):
    #Description:
    #The function calculate normalized correlation of two vectors
    # Input:
    #Ref - a refernce vector (Short or equel to Sig)
    #Sig - a vector to be checked
    #Short - if set, Do not check the macthed filters output, default - set
    #UseC - if set, use the c++ algorithm, default - set
    # Output:
    #MF - the normalized correlation's output
    ref, lRef=turnToVector(ref)
    sig, lSig=turnToVector(sig)
    if lRef>lSig:
        ref, sig=sig, ref
    pad = int(2 ** (np.ceil(np.log2(len(ref) + len(sig) + 1) )))
    ref=np.conjugate(ref-np.mean(ref))
    refPadded=np.zeros(pad, dtype=complex)
    refPadded[:len(ref)]=ref
    ref=refPadded

    #ref4fft = np.roll(refPadded, 1)
    ref4fft=ref[::-1]
    ref4fft=np.roll(ref4fft, 1)
    refFFTUp = np.fft.fft(ref4fft)
    sigmaSqrRef = sum(ref * np.conjugate(ref))
    #print(sigmaSqrRef, np.std(ref))
    sigmaRef = sum(ref)
    #print(sigmaRef)
    pos, MF, FixRefVal = normCorrSync(sig, refFFTUp, lRef, sigmaSqrRef, sigmaRef, short, useC)
    return MF


# %%
def normCorrSync(sig, refFFTUp, lRef, sigmaSqrRef, sigmaRef, short, useC):
    pickNum = 1;
    pickTH = 0.15;
    slopTH = 6;

    eps=2**(-52)

    pad = np.size(refFFTUp)
    lSig = np.size(sig);
    sigPadded=np.zeros(pad, dtype=complex)
    sigPadded[:len(sig)]=sig

    sigFft = np.fft.fft(sigPadded);
    sigmaXY = np.fft.ifft(sigFft * refFFTUp);
    sigmaSqrSig = np.zeros([1, lSig+1], dtype=complex)
    sigmaSig =np.zeros([1, lSig+1], dtype=complex)
    nCorr =np.zeros([1, lSig+1], dtype=complex)
    sigmaSqrSig=np.zeros(lSig, dtype=complex)
    sigmaSig=np.zeros(lSig, dtype=complex)
    nCorr=np.zeros(lSig, dtype=complex)
    sigmaSqrSig[0] = np.sum(sigPadded[0:lRef] * np.conjugate(sigPadded[0:lRef]));
    sigmaSig[0] = np.sum(sigPadded[0:lRef]);
    nCorrSig = sigmaSqrSig[0] - sigmaSig[0] * np.conjugate(sigmaSig[0]) / lRef
    nCorrRef = sigmaSqrRef - sigmaRef * np.conjugate(sigmaRef) / lRef
    nCorr[0] = (sigmaXY[0] - sigmaRef * sigmaSig[0] * lRef) / (np.sqrt(nCorrSig * nCorrRef))

    print(nCorrSig, nCorrRef, nCorr[0])
    for ind in range(1,lSig):
        sigmaSqrSig[ind] = sigmaSqrSig[ind - 1] - sigPadded[ind - 1] * np.conjugate(sigPadded[ind - 1]) + sigPadded[lRef + (ind - 1)] * np.conjugate(sigPadded[lRef + (ind - 1)]);
        sigmaSig[ind] = sigmaSig[ind - 1] - sigPadded[ind - 1] + sigPadded[lRef + (ind - 1)]
        nCorrSig = sigmaSqrSig[ind] - sigmaSig[ind] * np.conjugate(sigmaSig[ind]) / lRef
        nCorr[ind] = (sigmaXY[ind] - sigmaRef * sigmaSig[ind]* lRef) / (np.sqrt(nCorrSig * nCorrRef) + eps)
    pos = [];
    fixVal = [];
    MF = nCorr;
    return pos, MF, fixVal


def loadSignalFromFile(fname):
    if not os.path.isfile(fname):
        print("-E- no such file: " + fname)
        return None

    print("-I- processing " + fname)
    vec = np.fromfile(fname, sep=os.linesep)
    return vec
