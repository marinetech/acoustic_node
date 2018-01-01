class Log:
    def __init__(self, log_path):
      self.log_path = log_path
      open(self.log_path,'w').close()
      self.print_log("#...............initialyzing log...................")


    # Adds 'msg' to log.
    # if echo is true, also print 'msg' to console
    def print_log(self, msg, echo=True):
        log = open(self.log_path,'a')
        log.write(msg + "\n")
        log.close()
        if echo:
            print(msg)


if  __name__ == "__main__":
    log = Log("/home/ilan/projects/acoustic_node/rpi/test.log")
    for i in range(10):
        log.print_log("line #" + str(i))
