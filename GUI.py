#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 13:36:58 2021

@author: bing
"""

# import all the required  modules
import threading
import select
from tkinter import *
from tkinter import font
from tkinter import ttk
from chat_utils import *
import json
from PIL import Image, ImageTk, ImageGrab
import emoji
import socket
import requests
import urllib.request
import pickle
import gzip
import os
import binascii
import time
from tkinter import messagebox
from tkinter import filedialog
import random



# GUI class for the chat
class GUI:
    def __init__(self, send, recv, sm, s):
        self.Window = Tk()
        self.Window.withdraw()
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s
        self.my_msg = ""
        self.system_msg = ""

    def login(self):
        self.flag = False
        self.login_name = ''
        # login window
        self.login = Toplevel()
        self.login.title("Login")
        self.login.geometry('450x300')


        self.pls = Label(self.login, text="Please login to continue", font="Helvetica 14 bold", bg="white")
        self.pls.place(x=60, y=65)

        self.labelName = Label(self.login, text="Username: ", font="Helvetica 12", bg="white")
        self.labelName.place(x=90, y=130)
        self.labelPwd = Label(self.login, text="Password: ", font="Helvetica 12", bg="white")
        self.labelPwd.place(x=90, y=170)

        self.var_usr_name = StringVar()
        self.entry_usr_name = Entry(self.login, textvariable=self.var_usr_name)
        self.entry_usr_name.place(x=180, y=130)
        self.var_usr_pwd = StringVar()
        self.entry_usr_pwd = Entry(self.login, textvariable=self.var_usr_pwd, show='*')
        self.entry_usr_pwd.place(x=180, y=170)

        self.bt_login = Button(self.login, text='Login', command=lambda: self.usr_log_in(self.var_usr_name.get(), self.var_usr_pwd.get()))
        self.bt_login.place(x=110, y=230)
        self.bt_logreg = Button(self.login, text='Registration', command=lambda: self.usr_sign_up())
        self.bt_logreg.place(x=180, y=230)
        self.bt_logquit = Button(self.login, text='Quit', command=lambda: self.usr_sign_quit())
        self.bt_logquit.place(x=290, y=230)

        self.Window.mainloop()

    def usr_log_in(self, var_usr_name, var_usr_pwd):
        usr_name = var_usr_name
        usr_pwd = var_usr_pwd

        try:
            with open('usr_info.pickle', 'rb') as usr_file:
                usrs_info = pickle.load(usr_file)
        except FileNotFoundError:
            with open('usr_info.pickle', 'wb') as usr_file:
                usrs_info = {'admin': 'admin'}
                pickle.dump(usrs_info, usr_file)

        if usr_name == '' or usr_pwd == '':
            messagebox.showerror(message='Username or password is empty.')

        if usr_name in usrs_info:
            if usr_pwd == usrs_info[usr_name]:
                messagebox.showinfo(message='Welcome ' + usr_name + '!')
                self.flag = True
                self.login_name = usr_name
                self.gopage = Toplevel(self.login)
                self.gopage.title("CHATROOM")
                self.gopage.geometry('450x300')
                self.wel = Label(self.gopage, text="Welcome to Our Chatroom!", font="Helvetica 14 bold")
                self.wel.place(x=60, y=65)
                self.go = Button(self.gopage, text="CONTINUE", font="Helvetica 14 bold", command=lambda: self.goAhead(self.login_name))
                self.go.place(x=80, y=120)
            else:
                messagebox.showerror(message='Incorrect password.')
        else:
            is_signup = messagebox.askyesno(message='You have not registered yet, would you like to register now?')
            if is_signup:
                self.usr_sign_up()

    def usr_sign_up(self):
        def signtoreg():
            nn = var_new_name.get()
            np = var_new_pwd.get()
            npf = var_new_pwd_confirm.get()

            try:
                with open('usr_info.pickle', 'rb') as usr_file:
                    exist_usr_info = pickle.load(usr_file)
            except FileNotFoundError:
                exist_usr_info = {}

            if nn in exist_usr_info:
                messagebox.showerror('Error!', 'Username already exists.')
            elif np == '' or nn == '':
                messagebox.showerror('Error!', 'Username or password is empty.')
            elif np != npf:
                messagebox.showerror('Error!', 'Inconsistent passwords.')
            else:
                messagebox.showinfo('Registered successfully!', 'Welcome!')
                self.flag = True
                self.login_name = nn
                window_sign_up.destroy()
                exist_usr_info[nn] = np
                with open('usr_info.pickle', 'wb') as usr_file:
                    pickle.dump(exist_usr_info, usr_file)
                self.gopage = Toplevel(self.login)
                self.gopage.title("CHATROOM")
                self.gopage.geometry('450x300')
                self.wel = Label(self.gopage, text="Welcome to Our Chatroom!", font="Helvetica 14 bold")
                self.wel.place(x=60, y=65)
                self.go = Button(self.gopage, text="CONTINUE", font="Helvetica 14 bold", command=lambda: self.goAhead(self.login_name))
                self.go.place(x=80, y=120)

        window_sign_up = Toplevel(self.login)
        window_sign_up.geometry('350x200')
        window_sign_up.title('Registration')

        var_new_name = StringVar()
        new_name = Label(window_sign_up, text='Username：').place(x=10, y=10)
        enter_new_name = Entry(window_sign_up, textvariable=var_new_name).place(x=150, y=10)

        var_new_pwd = StringVar()
        new_pwd = Label(window_sign_up, text='Password：').place(x=10, y=50)
        enter_new_pwd = Entry(window_sign_up, textvariable=var_new_pwd, show='*').place(x=150, y=50)

        var_new_pwd_confirm = StringVar()
        new_pwd_confirm = Label(window_sign_up, text='Confirm Password：').place(x=10, y=90)
        enter_new_pwd_confirm = Entry(window_sign_up, textvariable=var_new_pwd_confirm, show='*').place(x=150, y=90)

        bt_confirm_sign_up = Button(window_sign_up, text='Complete Registration', command=signtoreg)
        bt_confirm_sign_up.place(x=150, y=130)

        window_sign_up.mainloop()
    
    
    def usr_sign_quit(self):
        self.login.destroy()
    
    def goAhead(self, name):
        if len(name) > 0:
            msg = json.dumps({"action":"login", "name": name})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                self.login.destroy()
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(name)
                self.layout(name)
                self.textCons.config(state = NORMAL)
                # self.textCons.insert(END, "hello" +"\n\n")   
                self.textCons.insert(END, menu +"\n\n")      
                self.textCons.config(state = DISABLED)
                self.textCons.see(END)
                # while True:
                #     self.proc()
        # the thread to receive messages
            process = threading.Thread(target=self.proc)
            process.daemon = True
            process.start()  
    # The main layout of the chat
    def layout(self,name):
        
        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width = False,
                              height = False)
        self.Window.configure(width = 470,
                              height = 550,
                              bg = "#17202A")
        self.labelHead = Label(self.Window,
                             bg = "#17202A", 
                              fg = "#EAECEE",
                              text = self.name ,
                               font = "Helvetica 13 bold",
                               pady = 5)
          
        self.labelHead.place(relwidth = 1)
        self.line = Label(self.Window,
                          width = 450,
                          bg = "#ABB2B9")
          
        self.line.place(relwidth = 1,
                        rely = 0.07,
                        relheight = 0.012)
          
        self.textCons = Text(self.Window,
                             width = 20, 
                             height = 2,
                             bg = "#17202A",
                             fg = "#EAECEE",
                             font = "Helvetica 14", 
                             padx = 5,
                             pady = 5)
          
        self.textCons.place(relheight = 0.745,
                            relwidth = 1, 
                            rely = 0.08)
          
        self.labelBottom = Label(self.Window,
                                 bg = "#ABB2B9",
                                 height = 80)
          
        self.labelBottom.place(relwidth = 1,
                               rely = 0.825)
          
        self.entryMsg = Entry(self.labelBottom,
                              bg = "#2C3E50",
                              fg = "#EAECEE",
                              font = "Helvetica 13")
          
        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth = 0.74,
                            relheight = 0.06,
                            rely = 0.008,
                            relx = 0.011)
          
        self.entryMsg.focus()
          
        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text = "Send",
                                font = "Helvetica 10 bold", 
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.sendButton(self.entryMsg.get()))
          
        self.buttonMsg.place(relx = 0.77,
                             rely = 0.008,
                             relheight = 0.06, 
                             relwidth = 0.22)
          
        self.textCons.config(cursor = "arrow")
          
        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)
          
        # place the scroll bar 
        # into the gui window
        scrollbar.place(relheight = 1,
                        relx = 0.974)
          
        scrollbar.config(command = self.textCons.yview)
          
        self.textCons.config(state = DISABLED)
  
    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state = DISABLED)
        self.my_msg = msg
        # print(msg)
        self.entryMsg.delete(0, END)

    def proc(self):
        # print(self.msg)
        while True:
            read, write, error = select.select([self.socket], [], [], 0)
            peer_msg = []
            # print(self.msg)
            if self.socket in read:
                peer_msg = self.recv()
            if len(self.my_msg) > 0 or len(peer_msg) > 0:
                # print(self.system_msg)
                self.system_msg += self.sm.proc(self.my_msg, peer_msg)
                self.my_msg = ""
                self.textCons.config(state = NORMAL)
                self.textCons.insert(END, self.system_msg +"\n\n")      
                self.textCons.config(state = DISABLED)
                self.textCons.see(END)

    def run(self):
        self.login()
# create a GUI class object
if __name__ == "__main__": 
    g = GUI()