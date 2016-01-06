import tkinter as tk
from message import *
from states import *

class   LoginState(State):
    def __init__(self, parent, checker):
        super().__init__(parent)
        self.checker = checker
        self.initUI()

    def initUI(self):
        self.loginLabel = tk.Label(self, text="Login:")
        self.login = tk.Entry(self)
        self.passwordLabel = tk.Label(self, text="Password:")
        self.password = tk.Entry(self)
        self.sendButton = tk.Button(self, text="Login", command=self.send)
        self.error = tk.StringVar()
        self.errorUi = tk.Label(self, textvariable=self.error)
        self.loginLabel.pack()
        self.login.pack()
        self.passwordLabel.pack()
        self.password.pack()
        self.sendButton.pack()
        self.errorUi.pack()
        self.password.bind("<Return>", lambda e: self.send)
        self.login.bind("<Return>", lambda e: self.send)

    def send(self):
        self.checker._login = self.login.get()
        self.checker._password = self.password.get()
        self.checker.login.set()

    def _in(self, **kwargs):
        super()._in(**kwargs)
        self.login.focus()

class   ChatState(State):
    def __init__(self, parent):
        super().__init__(parent)
        self.channels = {}
        self.channel = None
        self.initUI()

    def initUI(self):
        self.sendFrame = tk.Frame(self)
        self.entry = tk.Entry(self.sendFrame)
        self.sendButton = tk.Button(self.sendFrame, text="Send")
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)
        self.sendButton.pack()
        self.sendFrame.pack(side=tk.BOTTOM, fill=tk.X)

    def bind(self, callback):
        def _callback(event = None):
            callback(self.entry.get())
            self.entry.delete(0, len(self.entry.get()))
        self.entry.bind("<Return>", _callback)
        self.sendButton.config(command=_callback)

    def selectChannel(self, name):
        try:
            if self.channel:
                self.channel.pack_forget()
            self.channel = self.channels[name]
        except KeyError:
            pass
        if self.channel:
            self.channel.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

    def getChannel(self, name):
        try:
            return self.channels[name]
        except KeyError:
            self.channels[name] = Channel(self)
            if not self.channel:
                self.selectChannel(name)
            return self.channels[name]

    def _in(self, **kwargs):
        super()._in(**kwargs)
        self.entry.focus()

class   MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple chat")
        self.geometry("640x480")
        self.minsize(width=640, height=480)
        self.states = StateMachine()
        self.chat = ChatState(self)
        self.states.push(self.chat)
        self.states.pack(fill=tk.BOTH, expand=tk.YES)

    def getChannel(self, name):
        return self.chat.getChannel(name)

    def bind(self, callback):
        self.chat.bind(callback)
