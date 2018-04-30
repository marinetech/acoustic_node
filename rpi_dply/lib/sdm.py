import socket
import subprocess
import json
import glob
import os
import os.path
import time
import sys
from time import sleep
import numpy as np
import scipy.io
from scipy import signal
from shutil import copyfile
sys.path.append("/home/pi/acoustic_node/lib")
import matlab


class SDM:
    def __init__(self, tasks_dir, done_dir, log):
        self.tasks_dir = tasks_dir
        self.log = log
        self.done_dir = done_dir
        self.log.print_log("-I- SDM obj was Initialized successfully")


    def load_conf(self, conf):

        self.log.print_log("-I- loading configuration from: " + conf)
        self.parsed_json = json.loads( open(conf).read() )

        # must have keys
        for key in ["config", "times_to_repeat", "sleep_time", "modem", "sdmsh_cfg_file", "sdmsh_cmd_file", "sdmsh_bin"]:
            if key not in self.parsed_json:
                self.log.print_log("-E- invalid configuration - '" + key + "' is missing")
                exit(1)

        self.log.print_log("-I- modem config: " + self.parsed_json["config"])
        self.log.print_log("-I- times_to_repeat: " + str(self.parsed_json["times_to_repeat"]))
        self.log.print_log("-I- modem ID: " + self.parsed_json["modem"])


    def check_ping(self, modemIP):
        self.log.print_log("-I- verifying link to modem")

        response = os.system("ping -c 8 " + modemIP + "  2>&1 >/dev/null")
        if response == 0:
            return
        else:
            self.log.print_log("-E- no connection to: " + modemIP)
            exit(1)


    def clean(self):
        if 'rx_out_folder' in self.parsed_json:
            rx_out_folder = self.parsed_json["rx_out_folder"]
            if os.path.isdir(rx_out_folder):
                print("-I- cleaning Rx folder")
                for f in os.listdir(rx_out_folder):
                    os.remove(rx_out_folder + "/" + f)


    def check_dependencies(self):
        self.log.print_log("-I- checking dependencies")

        #verify files existence
        for dependency in ["sdmsh_bin", "tx"]:
            if dependency in self.parsed_json:
                if not os.path.isfile(self.parsed_json[dependency]):
                    self.log.print_log("-E- missing dependency: " + self.parsed_json[dependency])
                    exit(1)

        #verify dirs existence
        sdmsh_dir = os.path.dirname(self.parsed_json["sdmsh_cfg_file"])
        if not os.path.isdir(sdmsh_dir):
            os.makedirs(sdmsh_dir)

        # if rx is required we must have a sample_rate
        if "rx_out_folder" in self.parsed_json:
            for key in ["rx_sample_rate", "rx_winlen"]:
                if key not in self.parsed_json:
                    self.log.print_log("-E- Rx is required but no " + key + " was provided")
                    exit(1)


        for dir in ["rx_out_folder", "detected_folder"]:
            if dir in self.parsed_json:
                rx_out = self.parsed_json[dir]
                if not os.path.isdir(rx_out):
                    os.makedirs(rx_out)

        #verify collaterals for post-processing
        if "post" in self.parsed_json:
             # if our configuration has 'post', the following should exsist as well
            for key in ["matlab_ref", "detected_folder", "rx_out_folder"]:
                if not key in self.parsed_json:
                    self.log.print_log("-E- missing dependency for post-processing: " + key)
                    exit(1)

            # verify that our mat file is actually where it should be
            if not os.path.isfile(self.parsed_json["matlab_ref"]):
                self.log.print_log("-E- invalid matlab_ref: " + self.parsed_json["matlab_ref"])
                exit(1)

            # verify that our post function exists
            if not hasattr(self , self.parsed_json["post"]):
                self.log.print_log("-E- unknown post-processing: " + self.parsed_json["post"])
                exit(1)


    def set_sdm_mode(self, modemIP):
        self.log.print_log("-I- setting SDM mode")
        shell = subprocess.Popen(["sh"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        sock = socket.create_connection((modemIP, 9200), 2)
        sock.send(b'ATP\n')
        out = sock.recv(1024)
        # print("-D- " + str(out))


    def run_sdm_config(self):
        sdm_batch_file = self.parsed_json["sdmsh_cfg_file"]
        with open(sdm_batch_file,'w') as w:
            w.write("stop\n")
            w.write("config " +  self.parsed_json["config"])

        shell = subprocess.Popen(["sh"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        cmd = self.parsed_json["sdmsh_bin"] + " " + self.parsed_json["modem"] + " -f " + sdm_batch_file + "\n"
        shell.stdin.write(cmd.encode('ascii'))
        shell.stdin.close()

        for l in shell.stdout:
            self.log.print_log("    FROM MODEM: " + str(l))


    def run_sdm_commands(self):
        sdm_batch_file = self.parsed_json["sdmsh_cmd_file"]
        for counter in range(self.parsed_json["times_to_repeat"]):
            with open(sdm_batch_file,'w') as w:
                w.write("stop\n")
                if 'tx' in self.parsed_json: #need to Tx?
                    w.write("tx " + str(self.parsed_json["tx"]) + "\n")
                if 'rx_out_folder' in self.parsed_json: #need to Rx?
                    out_name = self.parsed_json["rx_out_folder"] + "/" + self.parsed_json["rx_out_folder"]
                    self.out_file = out_name + str(counter)
                    w.write("rx " + str(self.parsed_json["rx_sample_rate"]*self.parsed_json["rx_winlen"]) + " " + self.out_file + "\n")

            shell = subprocess.Popen(["sh"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            cmd = self.parsed_json["sdmsh_bin"] + " " + self.parsed_json["modem"] + " -f " + sdm_batch_file + "\n"
            shell.stdin.write(cmd.encode('ascii'))
            shell.stdin.close()
            for l in shell.stdout:
                self.log.print_log("    FROM MODEM: " + str(l))
            # need to run post-processing?
            if "post" in self.parsed_json:
                post_func = self.connect_func = getattr(self, self.parsed_json["post"])
                # sleep(1)
                post_func(self.out_file)
            sleep(self.parsed_json["sleep_time"])


    def basic_post_processing(self, f):
        self.log.print_log("-I- basic_post_processing() ")
        basename = os.path.basename(f)

        matfile = matlab.load_mat(self.parsed_json["matlab_ref"])
        if matfile is None:
            exit(1)

        thershold = matfile['thershold']
        Fc = float(matfile['Fc'])
        Fs = float(matfile['Fs'])
        Factor = int(matfile['Factor'])
        bLPF = matfile['bLPF'].reshape((-1,))
        TxRef = matfile['TxRef'].reshape((-1,))
        TxRef_BB = matlab.convert2bb(TxRef, Fc, Fs, Factor, bLPF)

        # Read & analyze Rx files
        RxSig = matlab.loadSignalFromFile(f)
        # need to check that we didn't load an empty files
        if RxSig is None:
            exit(1)
        self.log.print_log("-D- shape: " + str(RxSig.shape))
        self.log.print_log("-I- start: pre_bb_norm")
        RxSig = matlab.pre_bb_norm(RxSig)
        self.log.print_log("-I- done")
        self.log.print_log("-I- start: convert2bb")
        RxSig_BB = matlab.convert2bb(RxSig, float(Fc), float(Fs), int(Factor), bLPF)
        self.log.print_log("-I- done")
        self.log.print_log("-I- start: normCorrC")
        mf = matlab.normCorrC(TxRef_BB, RxSig_BB)
        self.log.print_log("-I- done")
        self.log.print_log("-I- start: absolute")
        mf_vector_absolute = np.absolute(mf)
        self.log.print_log("-I- done")

        # if detection copy all processing stages to detected folder; from there it will be sent to mainland
        self.log.print_log("-I- start: absolute")
        if matlab.has_detection(mf, thershold):
            self.log.print_log("-I- detected: " + f)

            pre_bb_norm = self.parsed_json["rx_out_folder"] + "/" + basename + ".norm"
            np.savetxt(pre_bb_norm, RxSig)

            bb_real = self.parsed_json["rx_out_folder"] + "/" + basename + ".bb.real"
            np.savetxt(bb_real, np.real(RxSig_BB))
            bb_imag = self.parsed_json["rx_out_folder"] + "/" + basename + ".bb.imag"
            np.savetxt(bb_imag, np.imag(RxSig_BB))

            after_mf =  self.parsed_json["rx_out_folder"] + "/" + basename + ".mf"
            np.savetxt(after_mf, mf)

            mf_absolute = self.parsed_json["rx_out_folder"] + "/" + basename + ".mf.abs"
            np.savetxt(mf_absolute, mf_vector_absolute)

            for src in [pre_bb_norm, bb_real, bb_imag, after_mf, mf_absolute]:
                #dst = self.parsed_json["detected_folder"] + "/" + os.path.basename(src)
                copyfile(src,  self.done_dir + "/" + basename )
        copyfile(f,  self.done_dir + "/" + basename )
        self.log.print_log("-I- done")


    def process_tasks(self):
        self.log.print_log("-I- processing tasks")
        for conf in glob.glob(self.tasks_dir + "/*.json"):
            self.load_conf(conf)
            modemIP = "192.168.0." + self.parsed_json["modem"]
            self.check_ping(modemIP)
            self.check_dependencies()
            self.clean()
            self.set_sdm_mode(modemIP)
            self.run_sdm_config()
            self.run_sdm_commands()



if  __name__ == "__main__":
    import log
    my_log = log.Log("./stam.log")
    sdm = SDM('/home/ilan/projects/acoustic_node/rpi/tasks', my_log)
    sdm.process_tasks()
