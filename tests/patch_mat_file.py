import scipy.io

if __name__ == "__main__":

    mat_file = '../resources/RefForTankTest.mat'

    matlab_ref = scipy.io.loadmat(mat_file)
    matlab_ref["Fc"] = 12000
    matlab_ref["Fs"] = 62500
    matlab_ref["TxRef"] = matlab_ref["OneLFMSignal"]
    matlab_ref["thershold"] = 0.225

    scipy.io.savemat(mat_file, matlab_ref)
