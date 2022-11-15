import time
import socket
import select
import sys
import json
from chat_utils import *
import client_state_machine as csm
import argparse

#import pp_Chat

import threading

class Client():
    def __init__(self):
        parser = argparse.ArgumentParser(description='chat client argument')
        parser.add_argument('-d', type=str, default=None, help='server IP addr')
        args = parser.parse_args()

        self.peer = ''
        self.console_input = []
        self.state = S_OFFLINE
        self.system_msg = ''
        self.local_msg = ''
        self.peer_msg = ''
        self.args = args
        
        self.username = '' #to remember the username
        self.my_msg = '' #message you send
        self.cmd_msg = '' #command

    def quit(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def get_name(self):
        return self.name

    def init_chat(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
        svr = SERVER if self.args.d == None else (self.args.d, CHAT_PORT)
        self.socket.connect(svr)
        self.sm = csm.ClientSM(self.socket)

        #reading_thread = threading.Thread(target=self.read_input)
        #reading_thread.daemon = True
        #reading_thread.start()

    def shutdown_chat(self):
        return

    def send(self, msg):
        mysend(self.socket, msg)

    def recv(self):
        return myrecv(self.socket)

    def setmymsg(self, my_msg):# to send the message
        self.my_msg = my_msg 

    def setcmdmsg(self, cmd_msg):# to send the command
        self.cmd_msg = cmd_msg

    def get_msgs(self): #work with proc
        read, write, error = select.select([self.socket], [], [], 0)
        my_msg = self.my_msg
        self.setmymsg('')
        cmd_msg = self.cmd_msg
        self.setcmdmsg('')
        peer_msg = []
        #peer_code = M_UNDEF    for json data, peer_code is redundant
        #if len(self.console_input) > 0:
        #   my_msg = self.console_input.pop(0)
        if self.socket in read:
            peer_msg = self.recv()

        return my_msg, peer_msg, cmd_msg

    def output(self):
        if len(self.system_msg) > 0:
            print(self.system_msg)
            self.system_msg = ''

    def login(self):
        #my_msg, peer_msg = self.get_msgs()
        if len(self.username) > 0: #read username
            self.name = self.username
            msg = json.dumps({"action":"login", "name":self.name})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                self.state = S_LOGGEDIN
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(self.name)
                self.print_instructions()
                return (True)
            elif response["status"] == 'duplicate':
                self.system_msg += 'Duplicate username, try again'
                return False
        else:               # fix: dup is only one of the reasons
           return(False)



    def read_input(self):
        while True:
            text = sys.stdin.readline()[:-1]
            self.console_input.append(text) # no need for lock, append is thread safe

    def print_instructions(self):
        self.system_msg += menu

    def run_chat(self): #run on the thread mainloop
        self.init_chat()
        #self.system_msg += 'Welcome to ICS chat\n'
        #self.system_msg += 'Please enter your name: '
        self.output()
        while self.login() != True: #try to login if the state is offline
            self.output()
        self.system_msg += 'Welcome, ' + self.get_name() + '!'
        self.output()
        timecnt = 0
        while self.sm.get_state() != S_OFFLINE: #loop after logging in
            self.proc()
            self.output() #to terminal
            time.sleep(CHAT_WAIT)
            timecnt = timecnt + 1 
            # refresh the online lists
            if (timecnt >= 10) and (self.cmd_msg == ''):
                self.setcmdmsg('who')
                timecnt = 0
        self.quit()

#==============================================================================
# main processing loop
#==============================================================================
    def proc(self): #process the messages
        my_msg, peer_msg, cmd_msg = self.get_msgs()
        self.system_msg += self.sm.proc(cmd_msg, my_msg, peer_msg) #add the command parameter
