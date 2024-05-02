from tkinter import *
from tkinter import ttk
from CustomNotebook import CustomNotebook
from Tab import Tab



class GUI(Tk):
    def __init__(self):
        super().__init__()

        style = ttk.Style()
        style.theme_use("default")
        style.configure("CustomNotebook", background="#3e3e3e", borderwidth=0, relief="flat", padding=[0, 5, 0, 0])
        style.map("CustomNotebook.Tab", background=[("selected", "#1e1e1e")], foreground=[("selected", "white")])
        style.configure("CustomNotebook.Tab", background="#3e3e3e", foreground="white", padding=[10, 0, 3, 0])

        self.tabs = []
        self.title("Image Master")

        self.notebook = CustomNotebook()
        self.notebook.pack(expand=True, fill="both")
        self.add_tab()
        self.current_tab = self.tabs[self.notebook.index("current")]
        self.menu_bar()


    def add_tab(self):
        new_tab = Tab(self.notebook)
        self.notebook.add(new_tab, text="Tab {} ".format(self.notebook.index("end")))
        self.tabs.append(new_tab)
        self.current_tab = self.tabs[self.notebook.index("current")]
        print("current tab: ",self.notebook.index("current"))


    def menu_bar(self):
        menubar = Menu(self ,font=("monospace", 10),activebackground="gray", bg="#2e2e2e", fg="white", borderwidth=0, relief="flat")
        menu_file = Menu(menubar,bg="#2e2e2e", fg="white", borderwidth=0, relief="flat", tearoff=0)
        menu_file.add_command(label="New", activebackground="gray", command=self.add_tab)
        menu_file.add_command(label="Open", activebackground="gray", command=self.importimage)
        menu_file.add_command(label="Save", activebackground="gray", command=self.saveimage)
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=exit)
        menubar.add_cascade(label="File", menu=menu_file)
        self.config(menu=menubar)


    def importimage(self):
        self.tabs[self.notebook.index("current")].importimage()


    def saveimage(self):
        self.tabs[self.notebook.index("current")].saveimage()
