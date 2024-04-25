import numpy as np
from PIL import Image, ImageTk
import cv2

class image:
    def __init__(self,path):
        self.path = path
        self.npimage = cv2.imread(path);
        self.photoimage = self.convert_cv_to_photoimage(self.npimage)

    def convert_cv_to_photoimage(self, cv_image):
        if cv_image is None:
            print("Error: Input image is empty.")
            return None
        image_rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image_rgb)
        photo_image = ImageTk.PhotoImage(image=pil_image)
        return photo_image
    
    def show(self):
        cv2.imshow(self.path,self.npimage)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def filter_choose(self,filter):
        if len(filter)==1:
            if filter[0]=="flip":
                self.flip()
            elif filter[0]=="grayscale":
                print("graaaaaaaaay")
                self.grayscale()
            elif filter[0]=="sharpen":
                self.sharpen()
            elif filter[0]=="emboss":
                self.emboss()
            elif filter[0]=="edge_detect":
                self.edge_detect()
            elif filter[0]=="negative":
                self.negative()
            elif filter[0] == "delete_background":
                self.delete_background()
            elif filter[0] == "positive":
                self.positive()
            
        elif len(filter)==2:
            if filter[0]=="rotate": 
                self.rotate(filter[1])
            elif filter[0]=="blur":
                self.blur(filter[1])
        elif len(filter)==3:
            if filter[0]=="resize":
                self.resize(filter[1],filter[2])

        elif len(filter)==5:
            if filter[0]=="crop":
                self.crop(filter[1],filter[2],filter[3],filter[5])


    def resize(self,new_width,new_height):
        self.npimage = cv2.resize(self.npimage, (new_width, new_height))
        self.photoimage = self.convert_cv_to_photoimage(self.npimage)

    def crop(self,x1,x2,y1,y2):
        self.npimage = self.npimage[y1,y2,x1,x2]
        self.photoimage = self.convert_cv_to_photoimage(self.npimage)

    def rotate(self,direction):
        if direction == "clockwise":
            self.npimage = cv2.rotate(self.npimage, cv2.cv2.ROTATE_90_CLOCKWISE)
        elif direction == "counterclockwise":
            self.npimage = cv2.rotate(self.npimage, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
        self.photoimage = self.convert_cv_to_photoimage(self.npimage)

    def flip(self):
        self.npimage = cv2.rotate(self.npimage, cv2.ROTATE_180)
        self.photoimage = self.convert_cv_to_photoimage(self.npimage)

    def grayscale(self):
        self.npimage = cv2.cvtColor(self.npimage, cv2.COLOR_BGR2GRAY)
        self.npimage = cv2.merge([self.npimage]*3)
        self.photoimage = self.convert_cv_to_photoimage(self.npimage)

    def blur(self,radius):
        
        radius=int(radius)
        if radius==1: 
            return
        # if radius % 2 == 0: radius += 1
        for i in range(radius):
            self.npimage = cv2.GaussianBlur(self.npimage, (5,5), 0)
        self.photoimage = self.convert_cv_to_photoimage(self.npimage)

    def sharpen(self):
        sharpening_kernel = np.array([[-1, -1, -1],
                               [-1,  9, -1],
                               [-1, -1, -1]])

        self.npimage = cv2.filter2D(self.npimage, -1, sharpening_kernel)
        self.photoimage = self.convert_cv_to_photoimage(self.npimage)

    def emboss(self):
        embossing_kernel = np.array([[-2, -1, 0],
                              [-1,  1, 1],
                              [ 0,  1, 2]])
        # Apply the embossing kernel to the image
        self.npimage = cv2.filter2D(self.npimage, -1, embossing_kernel)
        self.photoimage = self.convert_cv_to_photoimage(self.npimage)

    def edge_detect(self):
        gray_image = cv2.cvtColor(self.npimage, cv2.COLOR_BGR2GRAY)
        blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
        self.npimage = cv2.Canny(blurred_image, 50, 150)
        self.npimage = cv2.merge([self.npimage]*3)
        self.photoimage = self.convert_cv_to_photoimage(self.npimage)

    def negative(self):
        self.npimage = 255 - self.npimage
        self.photoimage = self.convert_cv_to_photoimage(self.npimage)

    def positive(self):
        self.npimage = 255 - self.npimage
        self.photoimage = self.convert_cv_to_photoimage(self.npimage)

    def delete_background(self):
        # Convert the image to grayscale
        gray_image = cv2.cvtColor(self.npimage, cv2.COLOR_BGR2GRAY)
        # Apply thresholding to create a binary mask
        _, mask = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)
        # Invert the mask
        mask = cv2.bitwise_not(mask)
        # Apply the inverted mask to the original image to make it negative
        self.npimage = cv2.bitwise_and(255 - self.npimage, 255 - self.npimage, mask=mask)
        # self.npimage = cv2.cvtColor(self.npimage, cv2.COLOR_GRAY2BGR)
        self.photoimage = self.convert_cv_to_photoimage(self.npimage)