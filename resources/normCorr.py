# -*- coding: utf-8 -*-
"""
Spyder Editor

normalized cross correlation functions by Roee Diamant
translated from matlab
"""

import numpy as np


def turnToVector(vec):    
    return vec.flatten(), np.size(vec.flatten())

def normCorrC(ref, sig, short, useC):
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