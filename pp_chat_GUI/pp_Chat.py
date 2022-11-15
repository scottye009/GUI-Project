from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
from tkinter import scrolledtext
import time
import pickle
from tkinter import ttk
import random
from chat_utils import *
from tkinter.constants import END

#from UP.chat_cmdl_client import Clasa
from threading import Thread
#import chat_cmdl_client as cmdl
from chat_client_class import Client


client = Client()
def create_thread():#to make multiple tasks run individually
    run_thread = Thread(target=client.run_chat)
    run_thread.setDaemon(True)
    run_thread.start()

create_thread()


root = Tk()
root.title('Login')
root.geometry('400x280')
#root.iconbitmap("pp1.icns")


def checkbutton_call(): #show password
    c = checkbutton_var.get()
    current = password_ent3.get()
    password_ent3.delete(0,END)
    if c == 0:
        password_ent3.configure(show = "*")
        password_ent3.insert(0,current)
        password_ent3.pack()
    else:
        password_ent3.configure(show="")
        password_ent3.insert(0,current)
        password_ent3.pack()

def checkuser(): #create the userinfo dictionary
    try:
        Database = open('userinfo.txt', 'rb')
        user_dict = pickle.load(Database)
        Database.close()
    except (FileNotFoundError, EOFError):
        user_dict = {}
        Database = open('userinfo.txt', 'wb')
        pickle.dump(user_dict, Database)
        Database.close()


#root.iconbitmap("images/1.")
def register_user():

    user_info = username.get()
    pass_info = password2.get()

    Database = open('userinfo.txt', 'rb')
    user_dict = pickle.load(Database)
    Database.close()
        
    user_dict[user_info] = pass_info
    Database = open('userinfo.txt', 'wb')
    pickle.dump(user_dict, Database)
    Database.close()
    
    password_ent1.delete(0,END)
    password_ent2.delete(0,END)
    username_ent.delete(0, END)

    Label(new, text="Registration successful!", fg='green').pack()

def check():
    Database = open('userinfo.txt', 'rb')
    user_dict = pickle.load(Database)
    Database.close()
    if password1.get() != password2.get():
        Label(new, text='Password does not match',fg='red').pack()
        password_ent1.delete(0,END)
        password_ent2.delete(0,END)
        username_ent.delete(0, END)
    
    elif username.get() in user_dict.keys():
        Label(new, text='Username has been used', fg='red').pack()
        password_ent1.delete(0, END)
        password_ent2.delete(0, END)
        username_ent.delete(0, END)

    else :
        register_user()
 
def popup(): #welcome
    
    msgbox = Tk()
    msgbox.withdraw()
    messagebox.showinfo("Hi", "Welcome to pp_Chat "+usernamev+"! \nDouble click the user online to chat. \nDouble click yourself to stop chatting.")
    #Label(root, text=response).grid()



def register():
    global new
    new = Toplevel(root)
    
    new.title('register')
    new.geometry('280x240')
    
    global username
    global password2
    global password1
    global username_ent
    global password_ent2
    global password_ent1

    username = StringVar()
    password1 = StringVar()
    password2 = StringVar()

    Label(new, text="Please enter your info below").pack()
    Label(new, text='').pack()
    Label(new, text='Set your username: * ').pack()
    username_ent = Entry(new, textvariable = username)
    username_ent.pack()
    
    Label(new, text='Set your password: * ').pack()
    password_ent1 = Entry(new, textvariable = password1 ,show='*')
    password_ent1.pack()
    Label(new, text='Confirm your password: * ').pack()
    password_ent2 = Entry(new, textvariable = password2 ,show='*')
    password_ent2.pack()
    username_ent.pack()

    Button(new, text='Submit', command=check).pack()

def login_ver():
    global usernamev
    usernamev = user_ver.get()
    passwordv = pass_ver.get()

    password_ent3.delete(0, END)
    username_ent1.delete(0, END)

    myfile = open('userinfo.txt','rb')
    userdict = pickle.load(myfile)
    myfile.close()
    if usernamev not in userdict.keys():
        Label(root, text='Username does not exist!', fg='red').pack()
    elif passwordv != userdict[usernamev]:
        Label(root, text='You entered the wrong password!', fg='red').pack()
    else:
        client.username = usernamev
        LOGIN_WAIT = 0.5 #wait for the server's response
        num = 0

        while client.state != S_LOGGEDIN: 
            time.sleep(LOGIN_WAIT)
            num = num +1
            if num > 5: 
                return

        root.destroy()
        popup()

        prim()

        #client.sm.set_state(S_OFFLINE)

        #time.sleep(2)


def prim():

    top = Toplevel()
    top.title('pp_Chat')
    top.geometry('580x600')
   
    def timesnow(): #showtime
        currentime = time.strftime("%H:%M:%S")
        timelabel.config(text= "Current Time: "+currentime)
        timelabel.after(1000, timesnow)

    timelabel = Label(top, font=("Courier", 10),bd=1, relief=SUNKEN, anchor=W)
    timelabel.grid(row=9,column=0,sticky=W)
    timesnow()
    #status = Label(top, text="Current Time: "+ str(len(image_list)), bd=1, relief=SUNKEN, anchor=E)
    
    def guessgame():
        
        num = random.randint(1,100)
        def checknum():
            
            #global out
            ent = e.get()
            
            if int(ent) > num:
                out = 'Too large'
                #a += 1
                Label(ggame, text=out).pack()
            elif int(ent) < num:
                out = 'Too small'
                #b += 1
                Label(ggame, text=out).pack()
            else:
                out = "Congrats you win!"
                Label(ggame, text=out).pack()

        ggame = Toplevel()
        ggame.title('GuessGame')
        ggame.geometry('520x540')
        Label(ggame, text="Please enter a number:").pack()
        e = Entry(ggame)
        e.pack()
        
        Button(ggame, text='Confirm', command=checknum).pack()
        Button(ggame, text="Restart", command=lambda:[ggame.destroy(), guessgame()]).pack()
        

    #tabcontrol===========
    global tab_chat
    global tab_poem
    global tab_calculator
    global tab_game
    global tab_searchhist
    global tab_settings
    
    wholetab = ttk.Notebook(top)
    tab_chat = ttk.Frame(wholetab)
    wholetab.add(tab_chat, text='Chat')
    tab_poem = ttk.Frame(wholetab)
    wholetab.add(tab_poem, text='Poem')
    tab_calculator = ttk.Frame(wholetab)
    wholetab.add(tab_calculator, text='Calculator')
    tab_game = ttk.Frame(wholetab)
    wholetab.add(tab_game, text='Game')
    tab_searchhist = ttk.Frame(wholetab)
    wholetab.add(tab_searchhist, text='Search History')
    tab_settings = ttk.Frame(wholetab)
    wholetab.add(tab_settings, text='Settings')

    wholetab.grid(row=0, column=0)



    #game
    guess_game = LabelFrame(tab_game, height = 100,width = 400,text="Guess Number")
    #low_f = LabelFrame(tab_game, height = 100,width = 400)  
    guess_game.grid(row=0, column=0)
    #low_f.grid(row=1, column=0)

    Label(guess_game, text="Try to guess a integer between 1 and 100 with the fewest attemps!").grid(row=0, column=0)
    Button(guess_game, text="Start", command=guessgame).grid(row=1, column=0, sticky=E)


    
    #Setting
    '''
    def set_rfont():
        pass
    def set_sfont():
        pass



    def set_rfontsize():
        pass
    def set_sfontsize():
        pass

    
    receivedmsg_setting = LabelFrame(tab_settings, height = 200,width = 300,text="Received Messages:")
    receivedmsg_setting.grid(row=1,column=1)
    Label(receivedmsg_setting, text="Choose a font size:").grid(column=1, row=1)
    receivedmsg_fs_var = StringVar()
    receivedmsg_fontsize = ttk.Combobox(receivedmsg_setting, width=12, textvariable=receivedmsg_fs_var, state="readonly")
    receivedmsg_fontsize['values'] = (10, 12, 14, 16, 22, 100)
    receivedmsg_fontsize.grid(column=2, row=1)
    receivedmsg_fontsize.current(1)

    Label(receivedmsg_setting, text="Choose a font:").grid(column=1, row=2)
    receivedmsg_f_var = StringVar()
    receivedmsg_font = ttk.Combobox(receivedmsg_setting, width=12, textvariable=receivedmsg_f_var, state="readonly")
    receivedmsg_font['values'] = ("Arial", "Comic Sans MS", "MS Serif", "Times New Roman")
    receivedmsg_font.grid(column=2, row=2)
    receivedmsg_font.current(3)

    sentmsg_setting = LabelFrame(tab_settings, height = 200,width = 300,text="Sent Messages:")
    sentmsg_setting.grid(row=2,column=1)
    Label(sentmsg_setting, text="Choose a font size:").grid(column=1, row=1)
    sentmsg_fs_var = StringVar()
    sentmsg_fontsize = ttk.Combobox(sentmsg_setting, width=12, textvariable=sentmsg_fs_var, state="readonly")
    sentmsg_fontsize['values'] = (10, 12, 14, 16, 22, 100)
    sentmsg_fontsize.grid(column=2, row=1)
    sentmsg_fontsize.current(1)
    Label(sentmsg_setting, text="Choose a font:").grid(column=1, row=2)
    sentmsg_f_var = StringVar()
    sentmsg_font = ttk.Combobox(sentmsg_setting, width=12, textvariable=sentmsg_f_var, state="readonly")
    sentmsg_font['values'] = ("Arial", "Comic Sans MS", "MS Serif", "Times New Roman")
    sentmsg_font.grid(column=2, row=2)
    sentmsg_font.current(3)
    '''

    background_setting = LabelFrame(tab_settings, height = 200,width = 300,text="Set background color:")
    background_setting.grid(row=3,column=1)

    Label(background_setting, text="Choose a background color:").grid(column=1, row=1)
    background_var = StringVar()
    background_set = ttk.Combobox(background_setting, width=12, textvariable=background_var, state="readonly")
    background_set['values'] = ["No background","AliceBlue", "AntiqueWhite","aquamarine","black","DarkGreen","lavender","MistyRose","YellowGreen"]
    background_set.grid(column=2, row=1)
    background_set.current(0)
    orig_color = top.cget("background")
    
    def callback(eventObject):
        c = background_set.get()
        if c == "No background":
            top.configure(background = orig_color)
        else:
            top.configure(background = c)
    
    background_set.bind("<<ComboboxSelected>>", callback)
    

    #poem=======================
    def get_poem():
        num = poem_number.get()
        client.setcmdmsg('p ' + str(num)) #send command to the server
        
    
    poem_number = Entry(tab_poem,  width=40)
    poem_number.insert(0, "Enter a number between 1 and 108: ")
    poem_number.grid(row=0, column=0, columnspan=1)

    Button(tab_poem, text="Fetch", command=get_poem).grid(row=0, column=1)

    poemdisframe = LabelFrame(tab_poem, width = 400, height = 480,text="Poem")
    poemdisframe.grid(row=1,column=0, columnspan=3)

    poem_display = scrolledtext.ScrolledText(poemdisframe, width = 70, height = 34)
    #poem_display.configure(state ='d
    # isabled')
    poem_display.grid(row=0,column=0)

    def poem_update(): #receive the poem
        if len(client.sm.poem_cont) > 0:
            strpoem = client.sm.poem_cont
            client.sm.clear_poem()
            poem_display.insert('1.0', strpoem)
        poem_display.after(2000, poem_update)

    poem_update()



    #search
    def search():
        word = chat_search.get()
        client.setcmdmsg('? ' + word)
        

    chat_search = Entry(tab_searchhist, width=40)
    chat_search.insert(0, "Enter the word you want to search: ")
    chat_search.grid(row=0, column=0)

    Button(tab_searchhist, text="Search", command=search).grid(row=0, column=1)
    
    histdisframe = LabelFrame(tab_searchhist, width = 400, height = 520,text="Chat History")
    histdisframe.grid(row=1,column=0, columnspan=3)

    hist_display = scrolledtext.ScrolledText(histdisframe, width = 70, height = 34)
    #hist_display.configure(state ='disabled')
    hist_display.grid(row=0,column=0)

    def histmsg_update(): 
        if len(client.sm.history_msg) > 0:
            strhistmsg = client.sm.history_msg
            client.sm.clear_historymsg()
            #hist_display.delete('1.0',END)
            hist_display.insert(END, strhistmsg)
        hist_display.after(2000, histmsg_update)

    histmsg_update()



    #Chat
    def send():
        currenttime = time.strftime("%H:%M:%S")
        client.setmymsg(text_send.get('1.0',END)) #send the message
        text_receive.insert(END, "["+currenttime+"][Myself] " + text_send.get('1.0',END)) #display the message you send
        text_send.delete('1.0',END)
        return

    def deletesent():
        text_send.delete('1.0', END)
    
    def connectto(self):
        toconnect = online_friends_lbox.get(online_friends_lbox.curselection()) #obtain the user for connection
        name = toconnect.split('-->')
        if name[0] == client.username: #self click to quit chat
            client.setcmdmsg('quitchat')
        else:
            client.setcmdmsg('c ' + toconnect) #click other to chat
        return
    
    def connectoff():
        offconnect = grp_friends_lbox.curselection()
        return
    

    def logout():
        client.setcmdmsg('logout')
        client.username = ''
        onlineval.set('')
        groupval.set('')
        logout_button.grid_forget() #disappear after clicking
        #login_button.grid(row = 0, column = 2, ipadx = 5)

    
    receive_f = LabelFrame(tab_chat, height = 100,width = 100, padx=2, text="Received Messages") 
    send_f = LabelFrame(tab_chat, height = 10,width = 10, padx=2,text="Textbox") 
    low_f = LabelFrame(tab_chat, height = 10,width = 30) 

    online_friends_lf = LabelFrame(tab_chat, height=10,width = 10,text="Online")  
    grp_friends_lf = LabelFrame(tab_chat, height = 10,width = 10,text="Group_Chat")  

    receive_f.grid(row=0, column = 0) 
    send_f.grid(row = 1,column = 0) 
    low_f.grid(row = 2,column = 0)    
    online_friends_lf.grid(row = 0,column = 1)
    grp_friends_lf.grid(row = 1,column = 1)

    wd_r = 15
    onlineval = StringVar()
    groupval = StringVar()
    online_friends_lbox = Listbox(online_friends_lf, listvariable=onlineval,height = 15, width = wd_r, font = ("Times New Roman",14))
    online_friends_lbox.bind('<Double-Button-1>', connectto)
    grp_friends_lbox = Listbox(grp_friends_lf, listvariable=groupval,height = 4, width = wd_r, font = ("Times New Roman",14))
    grp_friends_lbox.bind('<Double-Button-1>', connectoff)
    online_friends_lbox.pack(fill=BOTH)
    grp_friends_lbox.pack(fill=BOTH)

    wd = 44
    text_receive = scrolledtext.ScrolledText(receive_f, width = wd, height = 15, font = ("Times New Roman",15)) 
    #text_receive.configure(state ='disabled')
    text_receive.grid(row=0, column=0)
    
    text_send = scrolledtext.ScrolledText(send_f, width = wd, height = 4, font = ("Times New Roman",15)) 
    text_send.insert(INSERT,'')
    text_send.grid(row=1, column=0)

    clear_button = Button(low_f, text="Clear", command=deletesent)
    clear_button.grid(row = 0, column = 1, ipadx = 5)
    
    send_button = Button(low_f,text = 'Send',command = send, fg="royalblue2") 
    send_button.grid(row = 0, column = 0, ipadx = 5)

    logout_button = Button(low_f, text="Logout", command=logout, fg='red3')
    logout_button.grid(row = 0, column = 2, ipadx = 5)

    def online_update(): #update
        if client.sm.get_state() != S_OFFLINE:
            onlinedict=client.sm.logged_in
            onlinedict[client.username+'-->Myself']=0
        else:
            onlinedict = {}
        onlineval.set(list(onlinedict))
        online_friends_lbox.after(1000, online_update)

    online_update()

    def group_update():
        grouplist = []
        if client.sm.get_state() != S_OFFLINE:
            groupdict=client.sm.group
            for k in groupdict:
                grouplist = grouplist + groupdict[k]
            if client.username in grouplist:
                pass
            else:
                grouplist = []
        groupval.set(grouplist)
        grp_friends_lbox.after(1000, group_update)

    group_update()


    def recv_msg_append():
        if len(client.sm.recv_msg) > 0:
            currenttime = time.strftime("%H:%M:%S")
            text_receive.insert(END, "["+currenttime+"] " + client.sm.recv_msg)
            client.sm.clear_recvmsg()
        text_receive.after(100, recv_msg_append)

    recv_msg_append()



    #calculator =======================
    # ===============================
    e = Entry(tab_calculator, width=35, borderwidth=5)
    
    e.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

    def button_click(number):
        current = e.get()
        e.delete(0, END)
        e.insert(0, str(current) + str(number))

    def button_clear():
        e.delete(0, END)

    def button_add():
        first = e.get()
        global f_num
        global math
        math = "addition"
        f_num = float(first)
        e.delete(0, END)

    def button_equal():
        second = e.get()
        e.delete(0, END)
        if math == "addition":
            e.insert(0, f_num + float(second))

        if math == "subtration":
            e.insert(0, f_num - float(second))
        
        if math == "multiplication":
            e.insert(0, f_num * float(second))

        if math == "division":
            e.insert(0, f_num / float(second))

    def button_substract():
        first = e.get()
        global f_num
        global math
        math = "substract"
        f_num = float(first)
        e.delete(0, END)

    def button_multiply():
        first = e.get()
        global f_num
        global math
        math = "multiplication"
        f_num = float(first)
        e.delete(0, END)

    def button_divide():
        first = e.get()
        global f_num
        global math
        math = "division"
        f_num = float(first)
        e.delete(0, END)

    button_1 = Button(tab_calculator, text="1", padx=40, pady=20, command=lambda: button_click(1))
    button_2 = Button(tab_calculator, text="2", padx=40, pady=20, command=lambda: button_click(2))
    button_3 = Button(tab_calculator, text="3", padx=40, pady=20, command=lambda: button_click(3))
    button_4 = Button(tab_calculator, text="4", padx=40, pady=20, command=lambda: button_click(4))
    button_5 = Button(tab_calculator, text="5", padx=40, pady=20, command=lambda: button_click(5))
    button_6 = Button(tab_calculator, text="6", padx=40, pady=20, command=lambda: button_click(6))
    button_7 = Button(tab_calculator, text="7", padx=40, pady=20, command=lambda: button_click(7))
    button_8 = Button(tab_calculator, text="8", padx=40, pady=20, command=lambda: button_click(8))
    button_9 = Button(tab_calculator, text="9", padx=40, pady=20, command=lambda: button_click(9))
    button_0 = Button(tab_calculator, text="0", padx=97, pady=20, command=lambda: button_click(0))
    button_deci = Button(tab_calculator, text='.', padx=44, pady=20, command=lambda: button_click("."))
    button_add = Button(tab_calculator, text="+", padx=40, pady=20, command=button_add, highlightbackground='#3E4149')
    button_equal = Button(tab_calculator, text="=", padx=92, pady=20, command=button_equal)
    button_clear = Button(tab_calculator, text="Clear", padx=85, pady=20, command=button_clear)

    button_subtract = Button(tab_calculator, text="-", padx=40, pady=20, command=button_substract, highlightbackground='#3E4149')
    button_multiply = Button(tab_calculator, text="*", padx=40, pady=20, command=button_multiply, highlightbackground='#3E4149')
    button_divide = Button(tab_calculator, text="/", padx=40, pady=20, command=button_divide, highlightbackground='#3E4149')

    button_1.grid(row=3, column=0)
    button_2.grid(row=3, column=1)
    button_3.grid(row=3, column=2)

    button_4.grid(row=2, column=0)
    button_5.grid(row=2, column=1)
    button_6.grid(row=2, column=2)

    button_7.grid(row=1, column=0)
    button_8.grid(row=1, column=1)
    button_9.grid(row=1, column=2)

    button_0.grid(row=4, column=0, columnspan=2)
    button_deci.grid(row=4, column=2)

    button_clear.grid(row=5, column=0, columnspan=2)
    button_add.grid(row=1, column=3)
    button_equal.grid(row=5, column=2, columnspan=2)

    button_subtract.grid(row=2, column=3)
    button_multiply.grid(row=3, column=3)
    button_divide.grid(row=4, column=3)


    top.mainloop()



checkuser()

#Login ==========================================
global user_ver
global pass_ver
global username_ent1
global password_ent3

user_ver = StringVar()
pass_ver = StringVar()
checkbutton_var = IntVar()

Label(root, text="Welcome to pp_Chat!").pack()
#abel(root, text='').pack()

img = Image.open("pp.ico")
pic = ImageTk.PhotoImage(img)
Label(root, image=pic).pack()
Label(root, text='').pack()

Label(root, text='Enter your username: * ').pack()
username_ent1 = Entry(root, textvariable = user_ver)
username_ent1.pack()

Label(root, text='Enter your password: * ').pack()
password_ent3 = Entry(root, textvariable = pass_ver, show='*')
password_ent3.pack()

checkbutton = Checkbutton(root, text="show", variable=checkbutton_var,command=checkbutton_call)
checkbutton.deselect()
checkbutton.pack()

Button(root, text="Login", command=login_ver,  fg="royalblue2").pack()
#Button(root, text="Login", command=client).pack()
Button(root, text='Register', command=register, fg="slateblue2").pack()
#Button(root, text="Exit", command=root.quit).pack()

root.mainloop()

