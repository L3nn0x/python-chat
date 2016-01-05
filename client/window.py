import tkinter as tk
from message import *
from collections import defaultdict

class   MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple chat")
        self.geometry("640x480")
        self.minsize(width=640, height=480)
        self.initUI()
        self.channels = defaultdict(Channel)

    def initUI(self):
        self.sendFrame = tk.Frame(self)
        self.entry = tk.Entry(self.sendFrame)
        self.sendButton = tk.Button(self.sendFrame, text="Send")
        self.channel = Channel(self, 'general')
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)
        self.sendButton.pack()
        self.channel.pack(fill=tk.BOTH, expand=tk.YES)
        self.sendFrame.pack(side=tk.BOTTOM, fill=tk.X, expand=tk.YES)

    def bind(self, callback):
        self.sendButton.config(command=lambda: callback(self.entry.get()))
