import message
import sys
import os
import socket

class Bot:
    def __init__(self,botname,address,port,processfunc):
        self.Cookie = ""
        self.BotName = botname
        self.ProcessFunc = processfunc
        self.Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Sock.connect((address,port))
        message = "JOIN " + self.BotName + " password\n"
        self.Send(message)
    def Send(self,message) :
        self.Sock.sendall(message + "\n")
    def Run(self) :
        sockfile = os.fdopen(self.Sock.fileno())
        while True :
            temp = message.GetMessage(sockfile.readline())
            if temp.Type == "cookie" :
                self.Cookie = temp.Content
                continue
            if temp.From != "*ChatPi*" and temp.From != self.BotName :
                sendWhat, sure = self.ProcessFunc(temp)
                if sure :
                    msg = ""
                    if temp.Channel == "broadcast":
                        msg = "BROADCAST WITH " + self.Cookie + " " + sendWhat
                    else :
                        msg = "MSG WITH " + self.Cookie + " TO " + temp.From + " "+ sendWhat
                    self.Send(msg)
