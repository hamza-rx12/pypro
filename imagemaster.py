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
        
        self.frame1 = LabelFrame(self, text="Image: ", padx=10, pady=10, width=700, height=600, bg="#1e1e1e", fg="white")
        self.frame1.grid(row=0,column=0,padx=10,pady=10)
        self.frame1.pack_propagate(False)

        self.frame2 = LabelFrame(self, text="Tools: ", padx=10, pady=10, width=700, height=300, bg="#1e1e1e", fg="white")
        self.frame2.grid(row=1,column=0,padx=10,pady=10,columnspan=2)

        self.frame3 = LabelFrame(self, text="Bars", padx=10, pady=10, width=300, height=600, bg="#1e1e1e", fg="white",relief="groove")
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


        
        self.importIm = Button(self.frame1, text="Import Image", command=self.importimage, bg="#383838", fg="white")
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

    def show_image(self):
        if self.filename:  
            self.im = imageProcessor(self.filename)
            self.im.path = self.filename
            if self.im is not None:  
                self.lbl = Label(self.frame1, image=self.im.image.photoimage, bg="#1e1e1e")
                self.lbl.image = self.im.image.photoimage
                self.lbl.pack(padx=10, pady=10)
        else:
            print("No image selected")   

    def update_image(self, photoimage):
        if self.lbl:
            self.lbl.config(image=photoimage)
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