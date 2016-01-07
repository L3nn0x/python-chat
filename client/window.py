import tkinter as tk

from states import *
from message import Channel

LOGIN = 0
CHANNEL = 1

class   LoginState(State):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.ipLabel = tk.Label(self, text="IP:")
        self.ip = tk.Entry(self)
        self.ip.insert(tk.END, "127.0.0.1")
        self.portLabel = tk.Label(self, text="Port:")
        self.port = tk.Entry(self)
        self.port.insert(tk.END, "1234")
        self.port.pack(side=tk.BOTTOM)
        self.portLabel.pack(side=tk.BOTTOM)
        self.ip.pack(side=tk.BOTTOM)
        self.ipLabel.pack(side=tk.BOTTOM)
        self.loginLabel = tk.Label(self, text="Username:")
        self.loginUi = tk.Entry(self)
        self.passwordLabel = tk.Label(self, text="Password:")
        self.passwordUi = tk.Entry(self, show="*")
        self.loginLabel.pack()
        self.loginUi.pack()
        self.passwordLabel.pack()
        self.passwordUi.pack()
        self.button = tk.Button(self, text="Login", command=self.send)
        self.button.pack()
        self.error = tk.StringVar()
        self.errorLabel = tk.Label(self, textvariable=self.error)
        self.errorLabel.pack()
        self.passwordUi.bind("<Return>", lambda e: self.send())
        self.loginUi.bind("<Return>", lambda e: self.passwordUi.focus())

    def send(self):
        def _update(ok):
            if ok:
                self.error.set("Error: {}".format(ok))
        self.parent.notify((LOGIN, self.loginUi.get(), self.passwordUi.get(), self.ip.get(), self.port.get(), _update))

    def update(self, dt):
        self.error.set("")
        return True

    def _in(self, **kwargs):
        super()._in(**kwargs)
        self.loginUi.focus()

class   ChannelState(State):
    def __init__(self, parent, channel):
        super().__init__(parent)
        self.channel = channel
        self.initUI()

    def initUI(self):
        self.sendFrame = tk.Frame(self, bd=1)
        self.entry = tk.Entry(self.sendFrame)
        self.sendButton = tk.Button(self.sendFrame, text="Send", command=self.send)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)
        self.sendButton.pack()
        self.channel.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        self.sendFrame.pack(side=tk.BOTTOM, fill=tk.X)
        self.entry.bind("<Return>", lambda e: self.send())

    def update(self, dt):
        return True

    def send(self):
        self.parent.notify((CHANNEL, self.channel.name, self.entry.get()))
        self.entry.delete(0, len(self.entry.get()))

    def _in(self, **kwargs):
        super()._in(**kwargs)
        self.entry.focus()

    def _out(self):
        self.channel.pack_forget()
        super()._out()

class   MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple chat")
        self.geometry("640x480")
        self.minsize(width=640, height=480)
        self.channels = {}
        self.states = StateMachine()
        self.states.push(LoginState(self))
        self.states.pack(fill=tk.BOTH, expand=tk.YES)
        self.callback = None
        self.callbackIsAlive = None
        self.after(1000, self.checkAlive)

    def registerAlive(self, callback):
        self.callbackIsAlive = callback

    def cleanStates(self):
        self.states.popAll(1)

    def checkAlive(self):
        if self.callbackIsAlive:
            self.callbackIsAlive()
        self.states.update(1000)
        self.after(1000, self.checkAlive)

    def notify(self, data):
        if self.callback:
            self.callback(data)

    def register(self, callback):
        self.callback = callback
    
    def selectChannel(self, name):
        try:
            channel = self.channels[name]
        except KeyError:
            self.channels[name] = Channel(self, name)
        self.states.push(ChannelState(self, self.channels[name]))

    def getChannel(self, name):
        try:
            return self.channels[name]
        except KeyError:
            self.channels[name] = Channel(self, name)
            return self.channels[name]
