import paramiko
import stat
import os

class Network:
    def __init__(self, protocol, log):
      self.log = log
      self.protocol = protocol
      # check exitence of required fuunction for a given protocol e.g. 'ssh_connect', 'ssh_get' etc.
      for required_func in ["connect", "get", "put"]:
          if not hasattr(self , protocol + "_" + required_func):
              raise Exception("-E- protocol is not supported: " + protocol)

          self.connect_func = getattr(self, protocol + "_connect")
          self.get_func = getattr(self, protocol + "_get")
          self.put_func = getattr(self, protocol + "_put")

      self.log.print_log("-I- network obj was Initialized successfully [" + self.protocol + "]")



    def ssh_connect(self, ip, user, passwd):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.log.print_log("-I- ssh_connect: %s %s %s" % (ip, user, passwd))
        try:
            self.ssh.connect(ip, username=user, password=passwd)
        except  Exception as e:
            self.log.print_log("-E- ssh connection failed")
            self.log.print_log(str(e))
            exit(2)
        # stdin, stdout, stderr = self.ssh.exec_command('ls')
        # for line in stdout:
        #     self.log.print_log('... ' + line.strip('\n'))


    def ssh_get(self, remote_dir, local_dir):
        try:
            sftp = self.ssh.open_sftp()
            self.log.print_log("-I- pulling new tasks from: " + remote_dir)
            for attr in sftp.listdir_attr(remote_dir):
                if not stat.S_ISDIR(attr.st_mode): #if not directory
                    self.log.print_log(attr.filename)
                    sftp.get(remote_dir + "/" + attr.filename, local_dir + "/" + attr.filename)
            sftp.close()
        except  Exception as e:
            self.log.print_log("-E- ssh_get failed")
            self.log.print_log(str(e))
            exit(2)


    def ssh_put(self, remote_dir, local_dir):
        sftp = self.ssh.open_sftp()
        for f in os.listdir(local_dir):
            if os.path.isfile(local_dir + "/" + f):
                sftp.put(local_dir + "/" + f, remote_dir + "/" + f)
        sftp.close()



if  __name__ == "__main__":
    try:
        net = Network("ssh")
    except Exception as e:
        self.log.print_log(e)
        exit(1)
    #net.connect_func('127.0.0.1','pi','raspberry')
    net.connect_func('127.0.0.1','ilan','***REMOVED***')
    # net.ssh_get('/home/ilan/projects/acoustic_node/pc104_tasks', '/home/ilan/projects/acoustic_node/pc104_done/')
    net.ssh_put('/home/ilan/projects/acoustic_node/pc104_tasks', '/home/ilan/projects/acoustic_node/pc104_done/')
