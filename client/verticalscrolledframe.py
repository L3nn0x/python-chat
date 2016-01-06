import tkinter as tk

class   VerticalScrolledFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        scrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        self.canvas = canvas = tk.Canvas(self, bd=0, highlightthickness=0, yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        self.interior = interior = tk.Frame(canvas)
        scrollbar.config(command=canvas.yview)
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)
        interior_id = canvas.create_window(0, 0, anchor=tk.NW, window=interior)

        def _configure_interior(event):
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind("<Configure>", _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind("<Configure>", _configure_canvas)

        self.widgets = []

    def addWidget(self, widgetFactory, *args, **kwargs):
        scroll = False
        if int(self.canvas.yview()[1]) == 1 or not len(self.widgets):
            scroll = True
        self.widgets.append(widgetFactory(self.interior, *args, **kwargs))
        if scroll:
            self.scrollDown()
        return self.widgets[-1]

    def scrollDown(self):
        self.canvas.yview("moveto", "1.0")
