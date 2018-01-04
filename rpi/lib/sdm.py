import socket
import subprocess
import json
import glob
import os.path
import time

class SDM:
    def __init__(self, ip, port, tasks_dir, bin_dir ,log):
        self.ip = ip
        self.modemId = ip.split(".")[3]
        self.port = port
        self.tasks_dir = tasks_dir
        self.bin_dir = bin_dir
        self.log = log
        self.log.print_log("-I- SDM obj was Initialized successfully")

    def reset(self):
        sock = socket.create_connection((self.ip, 9200), 2)
        sock.send(b'AT?S\n')
        if (b'PHY' not in sock.recv(1024)):
              sock.send(b'ATP\n')
              sock.recv(1024)

    def runCMD(self, cmd):
        if cmd.startswith("sleep"):
            seconds = int(cmd.split(";")[1])
            print("sleep " + str(seconds))
            time.sleep(seconds)
            return

        print(cmd)
        shell = subprocess.Popen(["sh"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        with open('f.tmp','w') as w:
            w.write(cmd)
            cmdSh = self.bin_dir + "/sdmsh " + self.modemId + " -f f.tmp\n"
            shell.stdin.write(cmdSh.encode('ascii'))
        shell.stdin.close()
        # for l in shell.stdout:
        #     print(l)

    def parse_config(self, subtask):
        # print("__parse_config: " + str(subtask))
        for key in ["threshold", "gain", "level"]:
            if key not in subtask:
                print("-E- failed to parse subtask config - missing parameter: " + key)
                return None

        ret = ["config %s %s %s" % (subtask["threshold"], subtask["gain"], subtask["level"])]
        return ret

    def parse_tx(self, subtask):
        # print("__parse_tx: " + str(subtask))
        for key in ["signal", "loop", "sleep"]:
            if key not in subtask:
                print("-E- failed to parse subtask tx - missing parameter: " + key)
                return None

        if not os.path.isfile(self.tasks_dir + "/" + subtask["signal"]):
            print("-E- missing signal: " + subtask["signal"])
            return None

        if subtask["loop"] < 1:
            print("-E- invalid number of loops: " + str(subtask["loop"]))
            return None

        ret = []
        for i in range(subtask["loop"]):
            ret.append("tx " + self.tasks_dir + "/" + str(subtask["signal"]))
            if subtask["sleep"] > 0:
                ret.append("sleep;" + str(subtask["sleep"]))

        return ret

    def parse_rx(self, subtask):
        # print("__parse_rx: " + str(subtask))
        for key in ["ref", "Fs", "WinLen", "loop"]:
            if key not in subtask:
                print("-E- failed to parse subtask rx - missing parameter: " + key)
                return None

        if not os.path.isfile(self.tasks_dir + "/" + subtask["ref"]):
            print("-E- missing ref file: " + subtask["ref"])
            return None


        ret = ["ref " + self.tasks_dir + "/" + subtask["ref"]]
        for i in range(subtask["loop"]):
            ret.append("rx " + str(subtask["Fs"] * subtask["WinLen"]) + " " + subtask["ref"] + "_rx" + str(i))
        return ret

    def process_tasks(self):
        for task in glob.glob(self.tasks_dir + "/*.json"):
            # print(task)
            parsed_json = json.loads( open(task).read() )
            subtasks = []
            for subtask in parsed_json["task"]:
                try:
                    parse_func = getattr(self, "parse_" + subtask["cmd"])
                except:
                    print("-E- failed to parse %s - unknown cmd or cmd is missing" % (subtask)); exit(3)

                lines = parse_func(subtask)
                if lines == None:
                    print("-E- return val is None: %s" % (subtask)); exit(4)

                for line in lines:
                    subtasks.append(line)

            # And now to the execution part
            self.reset()
            for line in subtasks:
                self.runCMD(line)


if  __name__ == "__main__":
    sdm = SDM("192.168.0.149", '9200', '/home/ilan/projects/acoustic_node/rpi_tasks', '/home/ilan/projects/acoustic_node/rpi/bin', None)
    sdm.process_tasks()
