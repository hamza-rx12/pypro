import numpy as np
import cv2

class image:
    def __init__(self,path):
        self.path = path
        self.npimage = cv2.imread(path);

    def show(self):
        cv2.imshow(self.path,self.npimage)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    def filter_choose(self,filter):
        if filter=="resize":
            self.resize()
        elif filter=="crop":
            self.crop()
        elif filter=="rotate": 
            self.rotate()
        elif filter=="flip":
            self.flip()
        elif filter=="grayscale":
            self.grayscale()
        elif filter=="blur":
            self.blur()
        elif filter=="sharpen":
            self.sharpen()
        elif filter=="emboss":
            self.emboss()
        elif filter=="edge_detect":
            self.edge_detect()
        elif filter=="negative":
            self.negative()
        elif filter == "delete_background":
            self.delete_background()
        elif filter == "positive":
            self.positive()

    def resize(self,new_width,new_height):
        self.npimage = cv2.resize(self.npimage, (new_width, new_height))

    def crop(self,x1,x2,y1,y2):
        self.npimage = self.npimage[y1,y2,x1,x2]

    def rotate(self,direction):
        if direction == "clockwise":
            self.npimage = cv2.rotate(self.npimage, cv2.cv2.ROTATE_90_CLOCKWISE)
        elif direction == "counterclockwise":
            self.npimage = cv2.rotate(self.npimage, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)

    def flip(self,direction):
        self.npimage = cv2.rotate(self.npimage, cv2.ROTATE_180)

    def grayscale(self):
        self.npimage = cv2.cvtColor(self.npimage, cv2.COLOR_BGR2GRAY)

    def blur(self):
        self.npimage = cv2.GaussianBlur(self.npimage, (5, 5), 10)

    def sharpen(self):
        sharpening_kernel = np.array([[-1, -1, -1],
                               [-1,  9, -1],
                               [-1, -1, -1]])

        self.npimage = cv2.filter2D(self.npimage, -1, sharpening_kernel)

    def emboss(self):
        embossing_kernel = np.array([[-2, -1, 0],
                              [-1,  1, 1],
                              [ 0,  1, 2]])
# Apply the embossing kernel to the image
        self.npimage = cv2.filter2D(self.npimage, -1, embossing_kernel)

    def edge_detect(self):
        pass

    def negative(self):
        self.npimage = 255 - self.npimage

    def positive(self):
        self.npimage = 255 - self.npimage

    def delete_background(self):
        # Convert the image to grayscale
        gray_image = cv2.cvtColor(self.npimage, cv2.COLOR_BGR2GRAY)
        # Apply thresholding to create a binary mask
        _, mask = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)
        # Invert the mask
        mask = cv2.bitwise_not(mask)
        # Apply the inverted mask to the original image to make it negative
        self.npimage = cv2.bitwise_and(255 - self.npimage, 255 - self.npimage, mask=mask)
