"""
Created on Sun Apr  5 00:00:32 2015

@author: zhengzhang
"""
from chat_utils import *
import json
import ast

class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s
        self.logged_in = {} #read online
        self.group = {} #read group
        self.recv_msg = '' #message received
        self.poem_cont = '' # poem content
        self.history_msg = '' #historical messages

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state
    # clear contents once being processed
    def clear_poem(self):  #1
        self.poem_cont = ''

    def clear_historymsg(self): #2
        self.history_msg = ''

    def set_myname(self, name):
        self.me = name

    def clear_recvmsg(self): #3
        self.recv_msg = ''

    def get_myname(self):
        return self.me

    def get_loggedin(self): #external
        return self.logged_in

    def connect_to(self, peer): 
        msg = json.dumps({"action":"connect", "target":peer})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with '+ self.peer + '\n'
            self.recv_msg += 'You are connected with '+ self.peer + '\n' #messages to GUI
            return (True)
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
            self.recv_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot talk to yourself (sick)\n'
            self.recv_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
            self.recv_msg += 'User is not online, try again later\n'
        return(False)

    def disconnect(self):
        msg = json.dumps({"action":"disconnect"})
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''

    def proc(self, cmd_msg, my_msg, peer_msg): #add a parameter
        self.out_msg = ''
#==============================================================================
# Once logged in, do a few things: get peer listing, connect, search
# And, of course, if you are so bored, just go
# This is event handling instate "S_LOGGEDIN"
#==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(cmd_msg) > 0: #change command from my_msg to cmd_msg so you can chat and do other tasks simoutaneously

                if cmd_msg == 'logout':
                    self.out_msg += 'See you next time!\n'
                    self.group = {} #clear the chart
                    self.logged_in = {}
                    self.state = S_OFFLINE

                elif cmd_msg == 'time':
                    mysend(self.s, json.dumps({"action":"time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in

                elif cmd_msg == 'who':
                    mysend(self.s, json.dumps({"action":"list"})) #process the group info
                    who = json.loads(myrecv(self.s))["results"]
                    who = who.split('\n')
                    self.logged_in =ast.literal_eval(who[1])
                    if self.me in self.logged_in:
                        self.logged_in.pop(self.me)
                    self.group = ast.literal_eval(who[3])
                    #self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += who[1] + who[3]

                elif cmd_msg[0] == 'c':
                    peer = cmd_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer) == True:
                        self.state = S_CHATTING
                        self.out_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                        self.recv_msg += 'Connect to ' + peer + '. Chat away!\n\n' #notice on GUI
                        self.out_msg += '-----------------------------------\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'
                        self.recv_msg += 'Connection unsuccessful\n'

                elif cmd_msg[0] == '?':
                    term = cmd_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"search", "target":term}))
                    search_rslt = json.loads(myrecv(self.s))["results"].strip()
                    if (len(search_rslt)) > 0:
                        self.out_msg += search_rslt + '\n\n'
                        self.history_msg += search_rslt + '\n\n'
                    else:
                        self.out_msg += '\'' + term + '\'' + ' not found\n\n'
                        self.history_msg += '\'' + term + '\'' + ' not found\n\n'

                elif cmd_msg[0] == 'p':
                    poem_idx = cmd_msg[1:].strip() #get rid of the space first
                    if poem_idx.isdigit():
                        mysend(self.s, json.dumps({"action":"poem", "target":poem_idx}))
                        poem = json.loads(myrecv(self.s))["results"]
                        if (len(poem) > 0):
                            self.out_msg += poem + '\n\n'
                            self.poem_cont += poem + '\n\n'
                        else:
                            self.out_msg += 'Sonnet ' + poem_idx + ' not found\n\n'
                            self.poem_cont += 'Sonnet ' + poem_idx + ' not found\n\n'
                    else:
                        self.out_msg += menu

                else:
                    self.out_msg += menu

            if len(peer_msg) > 0:
                try:
                    peer_msg = json.loads(peer_msg)
                except Exception as err :
                    self.out_msg += " json.loads failed " + str(err)
                    return self.out_msg
            
                if peer_msg["action"] == "connect":

                    # ----------your code here------#
                    peer = peer_msg["from"]
                    self.peer += " " + peer
                    self.out_msg += "Request from " + peer + "\n"
                    self.out_msg += "You are connected with " + peer +  ".\n"
                    self.out_msg += 'Chat away!\n\n'
                    self.recv_msg += "Request from " + peer + "\n" #show status on GUI
                    self.recv_msg += "You are connected with " + peer +  ".\n"
                    self.recv_msg += 'Chat away!\n\n'
                    self.out_msg += '-----------------------------------\n'
                    self.state = S_CHATTING
                    # ----------end of your code----#
                    
#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_CHATTING: #copied from S_LOGGEDIN for doing multiple tasks while chatting
            if len(cmd_msg) > 0:

                if cmd_msg == 'quitchat':
                    mysend(self.s, json.dumps({"action":"disconnect"}))
                    self.out_msg += 'See you next time!\n'
                    self.state = S_LOGGEDIN
                if cmd_msg == 'logout':
                    #mysend(self.s, json.dumps({"action":"logout"}))
                    self.out_msg += 'See you next time!\n'
                    self.recv_msg += 'See you next time!\n'
                    self.group = {}
                    self.logged_in = {}
                    self.state = S_OFFLINE


                elif cmd_msg == 'time':
                    mysend(self.s, json.dumps({"action":"time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in

                elif cmd_msg == 'who':
                    try:
                        mysend(self.s, json.dumps({"action":"list"}))
                        who = json.loads(myrecv(self.s))["results"]
                        who = who.split('\n')
                        self.logged_in =ast.literal_eval(who[1])
                        if self.me in self.logged_in:
                            self.logged_in.pop(self.me)
                        self.group = ast.literal_eval(who[3])
                        #self.out_msg += 'Here are all the users in the system:\n'
                        self.out_msg += who[1] + who[3]
                    except:
                        pass

                elif cmd_msg[0] == 'c':
                    peer = cmd_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer) == True:
                        self.state = S_CHATTING
                        self.out_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                        self.recv_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                        self.out_msg += '-----------------------------------\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'
                        self.out_msg += 'Connection unsuccessful\n'

                elif cmd_msg[0] == '?':
                    term = cmd_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"search", "target":term}))
                    search_rslt = json.loads(myrecv(self.s))["results"].strip()
                    if (len(search_rslt)) > 0:
                        self.out_msg += search_rslt + '\n\n'
                        self.history_msg += search_rslt + '\n\n'
                    else:
                        self.out_msg += '\'' + term + '\'' + ' not found\n\n'
                        self.history_msg += '\'' + term + '\'' + ' not found\n\n'

                elif cmd_msg[0] == 'p':
                    poem_idx = cmd_msg[1:].strip()
                    if poem_idx.isdigit():
                        mysend(self.s, json.dumps({"action":"poem", "target":poem_idx}))
                        poem = json.loads(myrecv(self.s))["results"]
                        if (len(poem) > 0):
                            self.out_msg += poem + '\n\n'
                            self.poem_cont += poem + '\n\n'
                        else:
                            self.out_msg += 'Sonnet ' + poem_idx + ' not found\n\n'
                            self.poem_cont += 'Sonnet ' + poem_idx + ' not found\n\n'
                    else:
                        self.out_msg += menu

                else:
                    self.out_msg += menu #copy end

            if len(my_msg) > 0:     # my stuff going out
                mysend(self.s, json.dumps({"action":"exchange", "from":"[" + self.me + "]", "message":my_msg}))
                if my_msg == 'bye':
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''
            if len(peer_msg) > 0:    # peer's stuff, coming in

                # ----------your code here------#

                peer_msg = json.loads(peer_msg)

                if peer_msg["action"] == "exchange":
                    self.recv_msg += peer_msg["result"]
                    self.out_msg += self.recv_msg
                
                elif peer_msg["action"] == "connect":
                    self.out_msg += '(' + peer_msg["from"] + ' joined' + ')\n'
                    self.recv_msg += '(' + peer_msg["from"] + ' joined' + ')\n' #process info

                elif peer_msg["action"] == "disconnect":
                    self.out_msg += "Everyone left, you are alone.\n" 
                    self.recv_msg += "Everyone left, you are alone.\n" 
                    self.state = S_LOGGEDIN
                    self.disconnect()
                # ----------end of your code----#

            #Display the menu again
            if self.state == S_LOGGEDIN:
                self.out_msg += menu
#==============================================================================
# invalid state
#==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)

        return self.out_msg
