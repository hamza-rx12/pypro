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
        self.filename = None  # Initialize filename as None
        self.lbl = None #image label
        self.im = None
        self.title("Image Master")
        self.config(bg="#1e1e1e")
        
        self.frame1 = LabelFrame(self, text="Image: ", padx=10, pady=10, width=700, height=600, bg="#1e1e1e", fg="white")
        self.frame1.pack(padx=10,pady=10)
        
        self.frame2 = LabelFrame(self, text="Tools: ", padx=10, pady=10, width=700, height=300, bg="#1e1e1e", fg="white")
        self.frame2.pack(padx=10,pady=10)
        
        self.importIm = Button(self.frame1, text="Import Image", command=self.importimage, bg="#4CAF50", fg="white")
        self.importIm.place(relx=0.5, rely=0.5, anchor="center")
          # Initialize lbl as None

        # self.negative=Button(self.frame2, text="Negative", command=lambda: (self.im.applyFilter("edge_detect"),self.update_image(self.im.image.photoimage)), bg="#4CAF50", fg="white")
        # self.negative.pack()

        blur_var=BooleanVar()
        self.blur=CTkSwitch(self.frame2,text="Blur", variable=blur_var, command=lambda: self.on_click("blur",blur_var))
        self.blur.pack()
        
        edge_detect_var=BooleanVar()
        self.edge_detect=CTkSwitch(self.frame2,text="Edge detect", variable=edge_detect_var, command=lambda: self.on_click("edge_detect",edge_detect_var))
        self.edge_detect.pack()

        sharpen_var=BooleanVar()
        self.sharpen=CTkSwitch(self.frame2,text="Sharpen", variable=sharpen_var, command=lambda: self.on_click("sharpen",sharpen_var))
        self.sharpen.pack()

        grayscale_var=BooleanVar()
        self.grayscale=CTkSwitch(self.frame2,text="Grayscale", variable=grayscale_var, command=lambda: self.on_click("grayscale",grayscale_var))
        self.grayscale.pack()
    def on_click(self,filter,variable):
        if variable.get():

            self.im.applyFilter(filter)
            self.update_image(self.im.image.photoimage)
        else:
            self.im.revokeFilter(filter)
            self.update_image(self.im.image.photoimage)
        print("Variable value:", variable.get())
        print("Filter list:", self.im.filterList)

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
        self.image=image.image(self.path)
        self.filterList.append(filter)
        for fil in self.filterList:
            if filter=="grayscale" and "edge_detect" in self.filterList:
                pass
            elif filter=="edge_detect" and "grayscale" in self.filterList:
                pass
            else:
                self.image.filter_choose(fil)
    
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




    # def showimage(self):
    #     if self.filename:  # Check if a file was selected
    #         # Read the image using OpenCV
    #         self.image = imageProcessor(self.filename)
    #         self.image.path = self.filename
    #         if self.image is not None:  # Check if the image was successfully loaded
    #             # Convert the image from BGR to RGB format
    #             # image_rgb = cv2.cvtColor(self.image.image.npimage, cv2.COLOR_BGR2RGB)
    #             # Convert the image to PhotoImage format
    #             photo_image = self.convert_cv_to_photoimage(self.image.image.npimage)
    #             # If lbl already exists, destroy it before creating a new one
    #             if self.lbl:
    #                 self.lbl.destroy()
    #             # Create a new Label widget to display the image
    #             self.lbl = Label(self.frame1, image=photo_image, bg="#1e1e1e")
    #             self.lbl.image = photo_image
    #             self.lbl.pack(padx=10, pady=10)
    #         else:
    #             print("Error: Failed to load image")




# def convert_cv_to_photoimage(self, cv_image):
#         if cv_image is None:
#             print("Error: Input image is empty.")
#             return None
#         cv_image_rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    
#         # Convert the NumPy array to PIL Image format
#         pil_image = Image.fromarray(cv_image_rgb)
    
#         # Convert the PIL Image to PhotoImage format
#         photo_image = ImageTk.PhotoImage(image=pil_image)
    
#         return photo_image