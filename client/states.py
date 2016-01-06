import tkinter as tk

class   State(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

    def _in(self, **kwargs):
        self.pack(**kwargs)
        self.focus()

    def _out(self):
        self.pack_forget()

class   StateMachine:
    def __init__(self):
        self.states = []
        self.kwargs = None
        self.callback = None

    def pack(self, **kwargs):
        self.kwargs = kwargs
        if len(self.states):
            if kwargs:
                self.states[-1]._in(**kwargs)
            else:
                self.states[-1]._in()
    
    def push(self, state):
        if len(self.states):
            self.states[-1]._out()
        self.states.append(state)
        if self.kwargs:
            state._in(**self.kwargs)
        else:
            state._in()

    def pop(self):
        if not len(self.states):
            return
        self.states[-1]._out()
        self.states.pop()
        if len(self.states):
            if self.kwargs:
                self.states[-1]._in(**self.kwargs)
            else:
                self.states[-1]._in()

    def popAll(self, stop=0):
        while len(self.states) > stop:
            self.pop()
