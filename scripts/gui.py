from tkinter import *
from antikeylog import Process
from subprocess import Popen, PIPE
import os, signal
import psutil
from sys import stdout
from predict import DetectKeylogger
import time

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("AntiKeylogger")
        self.pack(fill=BOTH, expand=1)
        # write some text and explain what the program does
        text = Label(self, text="AntiKeylogger")
        text.place(x=150, y=50)
        text = Label(self, text="This program detects keyloggers and allows you to kill them")
        text.place(x=50, y=100)
        text = Label(self, text="Navigate using the functions menu")
        text.place(x=100, y=150)

        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu)
        file.add_command(label='Exit', command=self.client_exit)
        menu.add_cascade(label='File', menu=file)

        edit = Menu(menu)
        edit.add_command(label='Show all processes', command=self.show_processes)
        edit.add_command(label='Detect keylogger', command=self.show_keylogger_processes)
        menu.add_cascade(label='Functions', menu=edit)

    def client_exit(self):
        exit()

    def show_processes(self):
        # open a new window
        newWindow = Toplevel(self.master)
        newWindow.title("Processes---PID")
        newWindow.geometry("400x300")
        # get the process list
        process_list = Process.get_process_list()
        i=0
        for process in process_list:
            # display the process name and pid in the new window
            text = Label(newWindow, text=process['name'] + "---" + str(process['pid']))
            text.place(x=10, y=10+i)
            i+=20
    

    def show_keylogger_processes(self):
        # open a new window
        newWindow = Toplevel(self.master)
        newWindow.title("Detecting Keyloggers")
        newWindow.geometry("400x300")

        process_list = Process.get_process_list()
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
                if(x.find(y)>-1):
                    text = Label(newWindow, text="Keylogger Detected: " + x + "---" + str(process_pid[record]))
                    text.place(x=10, y=10)
                    flag=0
                    # kill the keylogger with a button
                    button = Button(newWindow, text="Kill Keylogger", command=lambda: Process.kill_logger(process_pid[record]))
                    button.place(x=10, y=50)


            record+=1
        if(flag):
            text = Label(newWindow, text="No Keylogger Detected")
            text.place(x=10, y=10)

root = Tk()
root.geometry("400x300")
app = Window(root)
root.mainloop()