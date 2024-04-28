import image
from tkinter import *
from tkinter import filedialog
from customtkinter import *
import os
import cv2
from PIL import Image,ImageTk



class GUI(Tk):
    def __init__(self):
        super().__init__()
        self.filename = None 
        self.lbl = None 
        self.im = None
        self.title("Image Master")
        self.config(bg="#1e1e1e")

        self.menu_bar()
        
        self.frame1 = LabelFrame(self, text="Image: ", padx=10, pady=10, width=700, height=600, bg="#1e1e1e", fg="white", font=("monospace", 10))
        self.frame1.grid(row=0,column=0,padx=10,pady=10)
        self.frame1.pack_propagate(False)

        self.frame2 = LabelFrame(self, text="Tools: ", padx=10, pady=10, width=700, height=300, bg="#1e1e1e", fg="white", font=("monospace", 10))
        self.frame2.grid(row=1,column=0,padx=10,pady=10,columnspan=2)

        self.frame3 = LabelFrame(self, text="Bars: ", padx=10, pady=10, width=300, height=600, bg="#1e1e1e", fg="white", font=("monospace", 10), relief="groove")
        self.frame3.grid(row=0,column=1,padx=10,pady=10,sticky='nsew')


        blur_intensity = DoubleVar()
        blur_intensity.set(1)
        self.bl=Label(self.frame3,text="Blur: ", bg="#1e1e1e", fg="white")
        self.blur_slider = CTkSlider(self.frame3,from_=1, to=21,
                                     number_of_steps=10,
                                     variable=blur_intensity,
                                     command=lambda x=blur_intensity.get(): self.on_slide("blur",x) if x==int(x) else None )
        self.blur_slider.grid(row=0,column=1)
        self.bl.grid(row=0,column=0)

        brightness_intensity = DoubleVar()
        brightness_intensity.set(0)
        self.brightness_label = Label(self.frame3, text="Brightness:", bg="#1e1e1e", fg="white")
        self.brightness_slider = CTkSlider(self.frame3, from_=-100, to=100, number_of_steps=10,
                                       variable=brightness_intensity,
                                       command=lambda x=brightness_intensity.get(): self.on_slide("brightness", x) if x==int(x) else None)
        self.brightness_label.grid(row=1, column=0, padx=(10, 0))
        self.brightness_slider.grid(row=1, column=1)

        red_saturation_factor = DoubleVar()
        red_saturation_factor.set(100)
        self.red_saturation_label = Label(self.frame3, text="Red Saturation:", bg="#1e1e1e", fg="white")
        self.red_saturation_slider = CTkSlider(self.frame3, from_=0, to=200,
                                               number_of_steps=10,
                                               variable=red_saturation_factor,
                                               command=lambda x=red_saturation_factor.get(): self.on_slide(
                                                   "adjust_red_saturation", x) if x == int(x) else None)
        self.red_saturation_label.grid(row=2, column=0, padx=(10, 0))
        self.red_saturation_slider.grid(row=2, column=1)

        green_saturation_factor = DoubleVar()
        green_saturation_factor.set(100)
        self.green_saturation_label = Label(self.frame3, text="Green Saturation:", bg="#1e1e1e", fg="white")
        self.green_saturation_slider = CTkSlider(self.frame3, from_=0, to=255,number_of_steps=10,
                                                 variable=green_saturation_factor,
                                                 command=lambda x=green_saturation_factor.get(): self.on_slide(
                                                     "adjust_green_saturation", x))
        self.green_saturation_label.grid(row=3, column=0, padx=(10, 0))
        self.green_saturation_slider.grid(row=3, column=1)

        blue_saturation_factor = DoubleVar()
        blue_saturation_factor.set(100)
        self.blue_saturation_label = Label(self.frame3, text="Blue Saturation:", bg="#1e1e1e", fg="white")
        self.blue_saturation_slider = CTkSlider(self.frame3, from_=0, to=200,
                                                variable=blue_saturation_factor,
                                                command=lambda x=blue_saturation_factor.get(): self.on_slide(
                                                    "adjust_blue_saturation", x))
        self.blue_saturation_label.grid(row=4, column=0, padx=(10, 0))
        self.blue_saturation_slider.grid(row=4, column=1)

        self.importIm = Button(self.frame1, text="Import Image", command=self.importimage, bg="#383838", fg="white", borderwidth=0, activebackground="gray")
        self.importIm.place(relx=0.5, rely=0.5, anchor="center")


        edge_detect_var=BooleanVar()
        self.edge_detect=CTkSwitch(self.frame2,text="Edge detect", variable=edge_detect_var, command=lambda: self.on_click(("edge_detect",),edge_detect_var))
        self.edge_detect.grid(row=0,column=1,padx=10,pady=10)

        sharpen_var=BooleanVar()
        self.sharpen=CTkSwitch(self.frame2,text="Sharpen", variable=sharpen_var, command=lambda: self.on_click(("sharpen",),sharpen_var))
        self.sharpen.grid(row=0,column=2,padx=10,pady=10)

        grayscale_var=BooleanVar()
        self.grayscale=CTkSwitch(self.frame2,text="Grayscale", variable=grayscale_var, command=lambda: self.on_click(("grayscale",),grayscale_var))
        self.grayscale.grid(row=0,column=3,padx=10,pady=10)

        emboss_var=BooleanVar()
        self.emboss=CTkSwitch(self.frame2,text="Emboss", variable=emboss_var, command=lambda: self.on_click(("emboss",),emboss_var))
        self.emboss.grid(row=0,column=4,padx=10,pady=10)

        negative_var=BooleanVar()
        self.negative=CTkSwitch(self.frame2,text="Negative", variable=negative_var, command=lambda: self.on_click(("negative",),negative_var))
        self.negative.grid(row=0,column=5,padx=10,pady=10)

    def menu_bar(self):
        menubar = Menu(self ,font=("monospace", 10),activebackground="gray", bg="#2e2e2e", fg="white", borderwidth=0, relief="flat")
        menu_file = Menu(menubar,bg="#2e2e2e", fg="white", borderwidth=0, relief="flat", tearoff=0)
        menu_file.add_command(label="New", activebackground="gray", command=None)
        menu_file.add_command(label="Open", activebackground="gray", command=self.importimage)
        menu_file.add_command(label="Save", activebackground="gray", command=self.saveimage)
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=exit)
        menubar.add_cascade(label="File", menu=menu_file)
        self.config(menu=menubar)

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
        # print("Variable value:", variable.get())
        # print("Filter list:", self.im.filterList)

    def importimage(self):
        self.filename = filedialog.askopenfilename(
            initialdir=".",  
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
            # self.im.image.photoimage = self.im.image.photoimage.subsample(2,2)
        else:
            print("No label found")




class imageProcessor:
    filterList=[]
    def __init__(self,path):
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
        else:
            self.filterList.append(filter)
            for fil in self.filterList:
                self.image.filter_choose(fil)
            print(self.filterList)

    def revokeFilter(self, filter):
        self.image=image.image(self.path)
        self.filterList.remove(filter)
        for fil in self.filterList:
            self.image.filter_choose(fil)

def main():
    app=GUI()
    icon_image = Image.open('./src/Imagemaster.png')
    icon_photo = ImageTk.PhotoImage(icon_image)
    app.iconphoto(True, icon_photo)
    app.mainloop()

if __name__ == "__main__":
    main()