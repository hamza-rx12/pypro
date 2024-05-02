import image
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from customtkinter import *
import os
import cv2
from PIL import Image,ImageTk

################################################################
#################          GUI CLASS            ################
################################################################

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
        # current_tab = self.tabs[self.notebook.index("current")]
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
        # self.filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        # self.tabs[self.notebook.index("current")].importimage()
        self.tabs[self.notebook.index("current")].importimage()

    def saveimage(self):
        # self.tabs[self.notebook.index("current")].saveimage()
        self.tabs[self.notebook.index("current")].saveimage()

################################################################
#################          TAB CLASS            ################
################################################################
class Tab(Frame):
    def __init__(self,master=None):
        super().__init__(master, bg="#2e2e2e")
        self.filename = None
        self.lbl = None
        self.im = None
        self.counter_left = 0
        self.counter_right = 0
        self.config(bg="#1e1e1e")

        self.frame1 = LabelFrame(self, text="Image: ", padx=10, pady=10, width=700, height=600, bg="#1e1e1e", fg="white", font=("monospace", 10))
        self.frame1.grid(row=0,column=0,padx=10,pady=10)
        self.frame1.pack_propagate(False)

        frame2 = LabelFrame(self, text="Tools: ", padx=10, pady=10, width=700, height=300, bg="#1e1e1e", fg="white", font=("monospace", 10))
        frame2.grid(row=1,column=0,padx=10,pady=10,columnspan=2)

        self.frame3 = LabelFrame(self, text="Bars: ", padx=10, pady=10, width=300, height=600, bg="#1e1e1e", fg="white", font=("monospace", 10), relief="groove")
        self.frame3.grid(row=0,column=1,padx=10,pady=10,sticky='nsew')


        #counterclockwise button
        rotate_counterclockwise_var = BooleanVar()
        rotate_counterclockwise_var.set(True)
        def increment_left(): self.counter_left = (self.counter_left+1)%4
        self.rotate_left_button = Button(self.frame3,text="Rotate Left",command=lambda : (increment_left(),self.on_click(("rotate_left",self.counter_left ),rotate_counterclockwise_var)))
        self.rotate_left_button.grid(row=0, column=0, sticky="e", padx=10)

        #clockwise rotate button
        rotate_clockwise_var = BooleanVar()
        rotate_clockwise_var.set(True)
        def increment_right(): self.counter_right = (self.counter_right+1)%4
        self.rotate_right_button = Button(self.frame3, text="Rotate Right",command=lambda : (increment_right(),self.on_click(("rotate_right",self.counter_right ),rotate_clockwise_var)))
        self.rotate_right_button.grid(row=0, column=1,padx=10,pady=10)

        #blur slider
        blur_intensity = DoubleVar()
        blur_intensity.set(1)
        self.bl=Label(self.frame3,text="Blur: ", bg="#1e1e1e", fg="white")
        self.blur_slider = CTkSlider(self.frame3,from_=1, to=21,
                                     number_of_steps=10,
                                     variable=blur_intensity,
                                     command=lambda x=blur_intensity.get(): self.on_slide("blur",x) if x==int(x) else None )
        self.blur_slider.grid(row=1,column=1)
        self.bl.grid(row=1,column=0, padx=(10, 0), pady=5, sticky='w')

        #brightness slider
        brightness_intensity = DoubleVar()
        brightness_intensity.set(0)
        self.brightness_label = Label(self.frame3, text="Brightness:", bg="#1e1e1e", fg="white")
        self.brightness_slider = CTkSlider(self.frame3, from_=-100, to=100, number_of_steps=10,
                                       variable=brightness_intensity,
                                       command=lambda x=brightness_intensity.get(): self.on_slide("brightness", x) if x==int(x) else None)
        self.brightness_label.grid(row=2, column=0, padx=(10, 0), pady=5, sticky='w')
        self.brightness_slider.grid(row=2, column=1)

        #contrast slider
        contrast_intensity = DoubleVar()
        contrast_intensity.set(0)
        self.contrast_label = Label(self.frame3, text="contrast:", bg="#1e1e1e", fg="white")
        self.contrast_slider = CTkSlider(self.frame3, from_=-50, to=50, number_of_steps=10,
                                       variable=contrast_intensity,
                                       command=lambda x=contrast_intensity.get(): self.on_slide("contrast", x) if x==int(x) else None)
        self.contrast_label.grid(row=3, column=0, padx=(10, 0), pady=5, sticky='w')
        self.contrast_slider.grid(row=3, column=1)

        #le slider pour la saturation de la couleur rouge
        red_saturation_factor = DoubleVar()
        red_saturation_factor.set(100)
        self.red_saturation_label = Label(self.frame3, text="Red Saturation:", bg="#1e1e1e", fg="white")
        self.red_saturation_slider = CTkSlider(self.frame3, from_=0, to=200,number_of_steps=10,
                                               variable=red_saturation_factor,
                                               command=lambda x=red_saturation_factor.get(): self.on_slide("red_saturation", x) if x == int(x) else None)
        self.red_saturation_label.grid(row=4, column=0, padx=(10, 0), pady=5, sticky='w')
        self.red_saturation_slider.grid(row=4, column=1)

        #le slider pour la saturation de la couleur verte
        green_saturation_factor = DoubleVar()
        green_saturation_factor.set(100)
        self.green_saturation_label = Label(self.frame3, text="Green Saturation:", bg="#1e1e1e", fg="white")
        self.green_saturation_slider = CTkSlider(self.frame3, from_=0, to=255,number_of_steps=10,
                                                 variable=green_saturation_factor,
                                                 command=lambda x=green_saturation_factor.get(): self.on_slide( "green_saturation", x))
        self.green_saturation_label.grid(row=5, column=0, padx=(10, 0), pady=5, sticky='w')
        self.green_saturation_slider.grid(row=5, column=1)

        #le slider pour la saturation de la couleur bleu
        blue_saturation_factor = DoubleVar()
        blue_saturation_factor.set(100)
        self.blue_saturation_label = Label(self.frame3, text="Blue Saturation:", bg="#1e1e1e", fg="white")
        self.blue_saturation_slider = CTkSlider(self.frame3, from_=0, to=200,variable=blue_saturation_factor,command=lambda x=blue_saturation_factor.get(): self.on_slide("blue_saturation", x))
        self.blue_saturation_label.grid(row=6, column=0, padx=(10, 0), pady=5, sticky='w')
        self.blue_saturation_slider.grid(row=6, column=1)

        #le boutton pour importer une image
        self.importIm = Button(self.frame1, text="Import Image", command=self.importimage, bg="#383838", fg="white", borderwidth=0, activebackground="gray")
        self.importIm.place(relx=0.5, rely=0.5, anchor="center")

        #boutton pour crop
        crop_var=StringVar()
        crop_var.set(False)
        self.crop_button = Button(self.frame3, text="Crop", command=lambda: self.on_click(("crop",),crop_var))
        self.crop_button.grid(row=0, column=2, padx=10,pady=10)

        edge_detect_var=BooleanVar()
        edge_detect=CTkSwitch(frame2,text="Edge detect", variable=edge_detect_var, command=lambda: self.on_click(("edge_detect",),edge_detect_var))
        edge_detect.grid(row=0,column=1,padx=10,pady=10)

        flip_var=BooleanVar()
        flip=CTkSwitch(frame2,text="flip", variable=flip_var, command=lambda: self.on_click(("flip",),flip_var))
        flip.grid(row=0,column=6,padx=10,pady=10)

        sharpen_var=BooleanVar()
        sharpen=CTkSwitch(frame2,text="Sharpen", variable=sharpen_var, command=lambda: self.on_click(("sharpen",),sharpen_var))
        sharpen.grid(row=0,column=2,padx=10,pady=10)

        grayscale_var=BooleanVar()
        grayscale=CTkSwitch(frame2,text="Grayscale", variable=grayscale_var, command=lambda: self.on_click(("grayscale",),grayscale_var))
        grayscale.grid(row=0,column=3,padx=10,pady=10)

        emboss_var=BooleanVar()
        emboss=CTkSwitch(frame2,text="Emboss", variable=emboss_var, command=lambda: self.on_click(("emboss",),emboss_var))
        emboss.grid(row=0,column=4,padx=10,pady=10)

        negative_var=BooleanVar()
        negative=CTkSwitch(frame2,text="Negative", variable=negative_var, command=lambda: self.on_click(("negative",),negative_var))
        negative.grid(row=0,column=5,padx=10,pady=10)

    def on_slide(self,*filter):
        self.im.applyFilter(filter)
        self.update_image(self.im.image.photoimage)

    def on_click(self,filter,variable):
        if variable.get():
            self.im.applyFilter(filter)
            self.update_image(self.im.image.photoimage)
        else:
            self.im.revokeFilter(filter)
            self.update_image(self.im.image.photoimage)
        self.update_image(self.im.image.photoimage)

        # print("Variable value:", variable.get())
        # print("Filter list:", self.im.filterList)

    def importimage(self):
        self.filename = filedialog.askopenfilename(
            initialdir="./src/",
            title="Select image file",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        self.show_image()

    def saveimage(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                 filetypes=[("JPEG files", "*.jpg"),
                                                            ("PNG files", "*.png"),
                                                            ("All files", "*.*")])
        if file_path:
            cv2.imwrite(file_path, self.im.image.npimage)
            print("Image saved successfully at:", file_path)

    def show_image(self):
        if self.filename:
            self.importIm.destroy()
            self.im = imageProcessor(self.filename)
            self.im.path = self.filename
            if self.im is not None:
                if self.lbl: self.lbl.destroy()
                self.lbl = Label(self.frame1, image=self.im.image.photoimage, bg="#1e1e1e")
                self.lbl.image = self.im.image.photoimage
                # self.lbl.pack(padx=10, pady=10, anchor="center", fill="none", expand=False)
                self.lbl.place(relx=0.5, rely=0.5, anchor="center")
        else:
            print("No image selected")

    def update_image(self, photoimage):
        if self.lbl:
            self.lbl.config(image=photoimage)
            self.im.image.photoimage = photoimage
            # self.im.image.photoimage = self.im.image.photoimage.subsample(2,2)

        else:
            print("No label found")



class imageProcessor:
    # filterList=[]
    def __init__(self,path):
        self.filterList=[]
        self.path=path
        self.image=image.image(path)

    def applyFilter(self,filter):
        filternames=list(map(lambda x: x[0],self.filterList))
        self.image=image.image(self.path)
        if len(filter)==2 :
            if filter[0] not in filternames:
                self.filterList.append(filter)
            else :
                self.filterList[filternames.index(filter[0])]=filter
            for fil in self.filterList:
                self.image.filter_choose(fil)
                print(self.filterList)
        elif len(filter)==1:
            if filter[0] not in filternames:
                self.filterList.append(filter)
            else :
                self.filterList.pop(filternames.index(filter[0]))
                self.filterList.append(filter)
            for fil in self.filterList:
                self.image.filter_choose(fil)
            print(self.filterList)
        else:
            self.filterList.append(filter)
            for fil in self.filterList:
                self.image.filter_choose(fil)
            print(self.filterList)

    def revokeFilter(self, filter):
        self.image = image.image(self.path)
        if filter in self.filterList:
            self.filterList.remove(filter)
        else:
            print("Filter not found in the list.")
        for fil in self.filterList:
            self.image.filter_choose(fil)


class CustomNotebook(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab"""

    __initialized = False

    def __init__(self, *args, **kwargs):
        if not self.__initialized:
            self.__initialize_custom_style()
            self.__inititialized = True

        kwargs["style"] = "CustomNotebook"
        ttk.Notebook.__init__(self, *args, **kwargs)

        self._active = None

        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""

        element = self.identify(event.x, event.y)

        if "close" in element:
            index = self.index("@%d,%d" % (event.x, event.y))
            self.state(['pressed'])
            self._active = index
            return "break"

    def on_close_release(self, event):
        """Called when the button is released"""
        if not self.instate(['pressed']):
            return

        element =  self.identify(event.x, event.y)
        if "close" not in element:
            # user moved the mouse off of the close button
            return

        index = self.index("@%d,%d" % (event.x, event.y))

        if self._active == index:
            self.forget(index)
            self.event_generate("<<NotebookTabClosed>>")

        self.state(["!pressed"])
        self._active = None

    def __initialize_custom_style(self):
        style = ttk.Style()
        self.images = (
            PhotoImage("img_close", data='''
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                '''),
            PhotoImage("img_closeactive", data='''
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                '''),
            PhotoImage("img_closepressed", data='''
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
            ''')
        )

        style.element_create("close", "image", "img_close",
                            ("active", "pressed", "!disabled", "img_closepressed"),
                            ("active", "!disabled", "img_closeactive"), border=8, sticky='')
        style.layout("CustomNotebook", [("CustomNotebook.client", {"sticky": "nswe"})])
        style.layout("CustomNotebook.Tab", [
            ("CustomNotebook.tab", {
                "sticky": "nswe",
                "children": [
                    ("CustomNotebook.padding", {
                        "side": "top",
                        "sticky": "nswe",
                        "children": [
                            ("CustomNotebook.focus", {
                                "side": "top",
                                "sticky": "nswe",
                                "children": [
                                    ("CustomNotebook.label", {"side": "left", "sticky": ''}),
                                    ("CustomNotebook.close", {"side": "left", "sticky": ''}),
                                ]
                        })
                    ]
                })
            ]
        })
    ])







def main():
    app=GUI()
    icon_image = Image.open('./src/Imagemaster.png')
    icon_photo = ImageTk.PhotoImage(icon_image)
    app.iconphoto(True, icon_photo)
    app.mainloop()

if __name__ == "__main__":
    main()















