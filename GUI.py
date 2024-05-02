from tkinter import *
from tkinter import ttk, messagebox
from CustomNotebook import CustomNotebook
from Tab import Tab



class GUI(Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Master")

        #CustomNotebook Styling
        #CustomNotebook is just a simple Notebook with a close button for each tab
        #We found it on Stackoverflow
        style = ttk.Style()
        style.theme_use("default")
        style.configure("CustomNotebook", background="#3e3e3e", borderwidth=0, relief="flat", padding=[0, 5, 0, 0])
        style.map("CustomNotebook.Tab", background=[("selected", "#1e1e1e")], foreground=[("selected", "white")])
        style.configure("CustomNotebook.Tab", background="#3e3e3e", foreground="white", padding=[10, 0, 3, 0])

        #Creating a Tab List
        self.tabs = []

        #Initializing the CustomNotebook
        self.notebook = CustomNotebook()
        self.notebook.pack(expand=True, fill="both")

        #Adding the Tabs
        self.add_tab()

        #Creating the Menu Bar
        self.menu_bar()


    def add_tab(self):
        new_tab = Tab(self.notebook)
        self.notebook.add(new_tab, text="Tab {} ".format(self.notebook.index("end")))
        self.tabs.append(new_tab)


    def menu_bar(self):
        menubar = Menu(self ,font=("monospace", 10),activebackground="gray", bg="#2e2e2e", fg="white", borderwidth=0, relief="flat")
        menu_file = Menu(menubar,bg="#2e2e2e", fg="white", borderwidth=0, relief="flat", tearoff=0)
        menu_file.add_command(label="New tab", activebackground="gray", command=self.add_tab)
        menu_file.add_command(label="Open image", activebackground="gray", command=self.importimage)
        menu_file.add_command(label="Save image", activebackground="gray", command=self.saveimage)
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=exit)
        menu_about = Menu(menubar,bg="#2e2e2e", fg="white", borderwidth=0, relief="flat", tearoff=0)
        menu_about.add_command(label="About", activebackground="gray", command=self.show_info)
        menubar.add_cascade(label="File", menu=menu_file)
        menubar.add_cascade(label="Help",menu=menu_about)
        self.config(menu=menubar)


    def importimage(self):
        self.tabs[self.notebook.index("current")].importimage()


    def saveimage(self):
        self.tabs[self.notebook.index("current")].saveimage()


    def show_info(self):
        info = """Image Master App
        
        Description:
        Image Master is an image processing application created using Tkinter, NumPy, OpenCV, and Pillow.
        
        Created By:
        - Hamza Alaoui Mhamdi
        - Oumaima Atmani
        
        Features:
        - Image manipulation and processing
        - Filters and effects
        - Cropping, resizing, and rotation
        
        Version: 1.0
        """
        messagebox.showinfo("App Information", info)
