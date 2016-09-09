import xml.sax as sax
import base64
from StringIO import StringIO

class Message:
    def __init__(self,Channel,From,Type,Content):
        self.Channel = Channel
        self.From = From
        self.Type = Type
        self.Content = Content
    def printMessage(self) :
        print "Message in channel ",self.Channel," from ",self.From, " of type ", self.Type
        print "==================================================="
        print self.Content

class Handler(sax.ContentHandler) :
    def __init__(self):
        self.CurrentData = ""
        self.Channel = ""
        self.From = ""
        self.Type = ""
        self.Content = ""
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "MESSAGE":
            self.Channel = attributes["CHANNEL"]
        if tag == "CONTENT":
            self.Type = attributes["TYPE"]
    def characters(self, content):
        if self.CurrentData == "FROM":
            self.From = content
        elif self.CurrentData == "CONTENT":
            self.Content = content
    def ReturnMessage(self):
        return Message(self.Channel,self.From,self.Type,base64.b64decode(self.Content))

def GetMessage(xmlmsg) :    
    parser = sax.make_parser()
    parser.setFeature(sax.handler.feature_namespaces, 0)
    H = Handler()
    parser.setContentHandler( H )
    parser.parse(StringIO(xmlmsg))
    m = H.ReturnMessage()
    return m
