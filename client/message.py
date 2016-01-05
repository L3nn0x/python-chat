import tkinter as tk
from verticalscrolledframe import *

class   Message(tk.Frame):
    def __init__(self, parent, source, data):
        super().__init__(parent, relief=tk.RAISED, borderwidth=1)
        self.source = source
        self.data = tk.StringVar()
        self._data = data
        self.data.set(data)
        self.id = None
        self.edited = False
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.dataUi = tk.Label(self, textvariable=self.data)
        self.sentUiLabel = tk.StringVar()
        self.sentUiLabel.set("sending...")
        self.sentUi = tk.Label(self, textvariable=self.sentUiLabel)
        self.sourceUi = tk.Label(self, text=self.source)
        self.dataUi.pack()
        self.sentUi.pack()
        self.sourceUi.pack()

    def sent(self, error = None):
        if not error:
            self.sentUiLabel.set("sent")
        else:
            self.sentUiLabel.set("Error: %s" % error)

    def edit(self, data):
        self.data.set(data)
        self.sentUiLabel.set("edited")


class   Channel(VerticalScrolledFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, True, *args, **kwargs)
        self.parent = parent
        self.messages = []

    def addMessage(self, source, data):
        self.messages.append(super().addWidget(Message, source, data))
        _id = len(self.messages)
        self.messages[-1].pack(fill=tk.X)
        return lambda error: self.messages[_id - 1].sent(error)

    def getMessage(self, source, data, id):
        for msg in self.messages:
            if msg.source == source and msg._data == data and msg.id == None:
                msg.id = id
                return
        self.addMessage(source, data)
        self.messages[-1].sentUiLabel.set("received")
        self.messages[-1].id = id

    def setHistory(self, history):
        for msg in history:
            self.getMessage(msg[1], msg[2], msg[0])
