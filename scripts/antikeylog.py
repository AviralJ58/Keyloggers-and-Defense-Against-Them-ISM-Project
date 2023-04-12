from subprocess import Popen, PIPE
import os, signal
import psutil
from sys import stdout
from predict import DetectKeylogger

class Process(object):
    if (DetectKeylogger.predict()):
        pid=os.getpid()

        def __init__(self, proc_info):
            self.user = proc_info[0]
            self.pid = proc_info[1]
            self.cpu = proc_info[2]
            self.mem = proc_info[3]
            self.vsz = proc_info[4]
            self.rss = proc_info[5]
            self.tty = proc_info[6]
            self.stat = proc_info[7]
            self.start = proc_info[8]
            self.time = proc_info[9]
            self.cmd = proc_info[10]

        def to_str(self):
            return '%s %s %s' % (self.user, self.pid, self.cmd)

        def name(self):
            return '%s' %self.cmd

        def procid(self):
            return '%s' %self.pid

        def kill_logger(key_pid):
            stdout.write("\n\nDo you want to stop this process: y/n ?"),
            response = input()
            if (response=="y" or response =="Y"):
                try:
                    os.kill(int(key_pid), signal.SIGILL)
                except OSError:
                    pass
            else:
                pass

        def get_process_list():
            process_list = []
            for proc in psutil.process_iter():
                #The separator for splitting is 'variable number of spaces'
                process_info = proc.as_dict(attrs=['pid', 'name'])
                process_list.append(process_info)
            return process_list

        if __name__ == "__main__":
            process_list = get_process_list()
            process_cmd=[]
            process_pid=[]
            for process in process_list:
                process_cmd.append(process['name'])
                process_pid.append(process['pid'])

            l1 = ["logkey","Keylogs","keysniff","kisni","lkl","ttyrpld","uber","vlogger","Keylogger.exe"]
            record=0
            flag=1
            for x in process_cmd:
                for y in l1:
                    if(x.find(y)>-1 and process_pid[record]!=pid):
                        print("KeyLogger Detected: \nThe following proccess may be a key logger: \n\n\t",process_pid[record]," ---> "+x)
                        kill_logger(process_pid[record])
                        flag=0
                        
                record+=1
        if(flag):
            print("No Keylogger Detected")