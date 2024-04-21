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
        # self.frame3.pack()


        blur_intensity = IntVar()
        blur_intensity.set(0)
        self.bl=Label(self.frame3,text="Blur: ", bg="#1e1e1e", fg="white")
        self.blur_slider = CTkSlider(self.frame3,from_=0, to=5, number_of_steps=5, variable=blur_intensity, command=lambda x=("blur",blur_intensity.get()): self.on_slide(x) )
        self.blur_slider.grid(row=0,column=1)
        self.bl.grid(row=0,column=0)


        
        self.importIm = Button(self.frame1, text="Import Image", command=self.importimage, bg="#4CAF50", fg="white")
        self.importIm.place(relx=0.5, rely=0.5, anchor="center")

        # blur_var=BooleanVar()
        # self.blur=CTkSwitch(self.frame2,text="Blur", variable=blur_var, command=lambda: self.on_click(("blur",),blur_var))
        # self.blur.grid(row=0,column=0,padx=10,pady=10)
        
        edge_detect_var=BooleanVar()
        self.edge_detect=CTkSwitch(self.frame2,text="Edge detect", variable=edge_detect_var, command=lambda: self.on_click(("edge_detect",),edge_detect_var))
        self.edge_detect.grid(row=0,column=1,padx=10,pady=10)

        sharpen_var=BooleanVar()
        self.sharpen=CTkSwitch(self.frame2,text="Sharpen", variable=sharpen_var, command=lambda: self.on_click(("sharpen",),sharpen_var))
        self.sharpen.grid(row=0,column=2,padx=10,pady=10)

        grayscale_var=BooleanVar()
        self.grayscale=CTkSwitch(self.frame2,text="Grayscale", variable=grayscale_var, command=lambda: self.on_click(("grayscale",),grayscale_var))
        self.grayscale.grid(row=0,column=3,padx=10,pady=10)

    def on_slide(self,filter):
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
            initialdir=".",  # Start in the current directory
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
        # self.lbl.config(image=photoimage);
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
        # print("filteeeeeer")
        self.image=image.image(self.path)
        self.filterList.append(filter)
        for fil in self.filterList:
            if filter==("grayscale",) and ("edge_detect",) in self.filterList:
                pass
            elif filter==("edge_detect",) and ("grayscale",) in self.filterList:
                pass
            else:
                self.image.filter_choose(fil)
            

            # if filter=="grayscale" and "edge_detect" in self.filterList:
            #     pass
            # elif filter=="edge_detect" and "grayscale" in self.filterList:
            #     pass
            # else:
    
    def revokeFilter(self, filter):
        self.image=image.image(self.path)
        self.filterList.remove(filter)
        for fil in self.filterList:
            self.image.filter_choose(fil)

def main():
    app=GUI()
    app.mainloop()

if __name__ == "__main__":
    main()