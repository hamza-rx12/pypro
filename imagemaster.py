import image
from tkinter import *
from tkinter import filedialog
import os
import cv2
from PIL import Image,ImageTk



class GUI(Tk):
    def __init__(self):
        super().__init__()
        self.filename = None  # Initialize filename as None
        self.image = image.image(self.filename)
        self.title("Image Master")
        self.config(bg="#1e1e1e")
        
        self.frame1 = LabelFrame(self, text="Image: ", padx=10, pady=10, width=700, height=600, bg="#1e1e1e", fg="white")
        self.frame1.pack(padx=10,pady=10)
        
        self.frame2 = LabelFrame(self, text="Tools: ", padx=10, pady=10, width=700, height=300, bg="#1e1e1e", fg="white")
        self.frame2.pack(padx=10,pady=10)
        
        self.importIm = Button(self.frame1, text="Import Image", command=self.importimage, bg="#4CAF50", fg="white")
        self.importIm.place(relx=0.5, rely=0.5, anchor="center")
        self.image = image.image(self.filename)

        self.negative=Button(self.frame2, text="Negative", command=lambda: self.negative(self.filename), bg="#4CAF50", fg="white")
        self.negative.place(relx=0.5, rely=0.5, anchor="center")
        
        self.lbl.image=self.convert_cv_to_photoimage(self.image.npimage)
        
    def importimage(self):
        self.filename = filedialog.askopenfilename(
            initialdir=".",  # Start in the current directory
            title="Select image file",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        
        if self.filename:  # Check if a file was selected
  # Read the image using OpenCV
            self.image.path = self.filename
            if self.image is not None:  # Check if the image was successfully loaded
                # Convert the image from BGR to RGB format
                image_rgb = cv2.cvtColor(self.image.npimage, cv2.COLOR_BGR2RGB)
                # Convert the image to PhotoImage format
                photo_image = self.convert_cv_to_photoimage(image_rgb)
                # If lbl already exists, destroy it before creating a new one
                if self.lbl:
                    self.lbl.destroy()
                # Create a new Label widget to display the image
                self.lbl = Label(self.frame1, image=photo_image, bg="#1e1e1e")
                self.lbl.image = photo_image
                self.lbl.pack(padx=10, pady=10)
            else:
                print("Error: Failed to load image")
    
    def convert_cv_to_photoimage(self, cv_image):
        pil_image = Image.fromarray(cv_image)
        # Convert the PIL Image to PhotoImage format
        photo_image = ImageTk.PhotoImage(image=pil_image)
        return photo_image

class imageProcessor:
    filterList=[]
    def __init__(self,path):
        self.path=path
        self.image=image.image(path)


    def applyFilter(self,filter):
        self.image=image.image(self.path)
        self.filterList.append(filter)
        for fil in self.filterList:
            self.image.filter_choose(fil)
    
    def revokeFilter(self, filter):
        image=image.image(self.path)
        self.filterList.remove(filter)
        for fil in self.filterList:
            self.image=self.image.filter_choose(fil)

def main():
    app=GUI()
    app.mainloop()

if __name__ == "__main__":
    main()