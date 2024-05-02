from tkinter import *
from customtkinter import *
import cv2
from ImageProcessor import *


class Tab(Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.filename = None
        self.lbl = None
        self.im = None
        self.counter_left = 0
        self.counter_right = 0
        self.config(bg="#1e1e1e")

        ################################################################
        #######################   FRAMES   #############################
        ################################################################

        #Image Frame
        self.frame1 = LabelFrame(self, text="Image: ", padx=10, pady=10, width=700, height=600, bg="#1e1e1e", fg="white", font=("monospace", 12))
        self.frame1.grid(row=0,column=0,padx=10,pady=10)
        self.frame1.pack_propagate(False)

        #Tools Frame
        self.frame2 = LabelFrame(self, text="Filters: ", padx=10, pady=10, width=700, height=300, bg="#1e1e1e", fg="white", font=("monospace", 12))
        self.frame2.grid(row=1,column=0,padx=10,pady=10,columnspan=2)

        #Bars Frame
        self.frame3 = LabelFrame(self, text="Tools: ", padx=10, pady=10, width=300, height=600, bg="#1e1e1e", fg="white", font=("monospace", 12), relief="groove")
        self.frame3.grid(row=0,column=1,padx=10,pady=10,sticky='nsew')

        ################################################################
        #######################   BUTTONS   ############################
        ################################################################

        #Place Holder variable:
        variable=BooleanVar()
        variable.set(True)

        #Import Button
        self.importIm = Button(self.frame1, text="Import Image", 
                               command=self.importimage, bg="#383838", fg="white", 
                               borderwidth=0, activebackground="gray",
                               font=("monospace", 10))
        self.importIm.place(relx=0.5, rely=0.5, anchor="center")

        #Left Rotation Button
        def increment_left(): self.counter_left = (self.counter_left+1)%4
        rotate_left_button = Button(self.frame3,text="Rotate Left",
                                         bg="#383838", fg="white", borderwidth=0, activebackground="gray",
                                         command=lambda : (increment_left(),self.on_click(("rotate_left",self.counter_left ),variable)),
                                         width=15, height=1, font=("monospace", 10))
        rotate_left_button.grid(row=0, column=0, sticky="e", padx=45)

        #Right Rotation Button
        def increment_right(): self.counter_right = (self.counter_right+1)%4
        rotate_right_button = Button(self.frame3, text="Rotate Right",
                                          bg="#383838", fg="white", borderwidth=0, activebackground="gray",
                                          command=lambda : (increment_right(),self.on_click(("rotate_right",self.counter_right ),variable)),
                                          width=15, height=1, font=("monospace", 10))
        rotate_right_button.grid(row=0, column=1,padx=10,pady=10)

        #Cropping Button
        def crop_():
            crop_box = cv2.selectROI(self.im.path, self.im.image.npimage)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return crop_box
        crop_button = Button(self.frame3, text="Crop", 
                                  bg="#383838", fg="white", borderwidth=0, activebackground="gray",
                                  command=lambda:self.on_click(("crop",crop_()),variable),
                                  width=15, height=1, font=("monospace", 10))
        crop_button.grid(row=1, column=0, padx=10,pady=10)

        #Flipping Button
        self.flip_counter = 0;
        def increment_flip(): self.flip_counter = (self.flip_counter + 1)%2
        flip_button = Button(self.frame3, text="Flip", 
                                  bg="#383838", fg="white", borderwidth=0, activebackground="gray",
                                  command=lambda: (increment_flip(),self.on_click(("flip",self.flip_counter),variable)),
                                  width=15, height=1, font=("monospace", 10))
        flip_button.grid(row=1, column=1, padx=10,pady=10)


        ################################################################
        #####################   CTK_SLIDERS   ##########################
        ################################################################

        #Blur Slider
        blur_intensity = DoubleVar()
        blur_intensity.set(1)
        bl=Label(self.frame3,text="Blur: ", bg="#1e1e1e", fg="white", font=("monospace", 12))
        blur_slider = CTkSlider(self.frame3,from_=1, to=21,
                                     number_of_steps=10,
                                     variable=blur_intensity,
                                     command=lambda x=blur_intensity.get(): self.on_slide("blur",x) if x==int(x) else None )
        blur_slider.grid(row=2,column=1)
        bl.grid(row=2,column=0, padx=(10, 0), pady=5, sticky='w')

        #Brightness Slider
        brightness_intensity = DoubleVar()
        brightness_intensity.set(0)
        brightness_label = Label(self.frame3, text="Brightness:", bg="#1e1e1e", fg="white", font=("monospace", 12))
        brightness_slider = CTkSlider(self.frame3, from_=-100, to=100, number_of_steps=10,
                                       variable=brightness_intensity,
                                       command=lambda x=brightness_intensity.get(): self.on_slide("brightness", x) if x==int(x) else None)
        brightness_label.grid(row=3, column=0, padx=(10, 0), pady=5, sticky='w')
        brightness_slider.grid(row=3, column=1)

        #Red Saturation Slider
        red_saturation_factor = DoubleVar()
        red_saturation_factor.set(100)
        red_saturation_label = Label(self.frame3, text="Red Saturation:", bg="#1e1e1e", fg="white", font=("monospace", 12))
        red_saturation_slider = CTkSlider(self.frame3, from_=0, to=200,number_of_steps=10,
                                               variable=red_saturation_factor,
                                               command=lambda x=red_saturation_factor.get(): self.on_slide("red_saturation", x) if x == int(x) else None)
        red_saturation_label.grid(row=4, column=0, padx=(10, 0), pady=5, sticky='w')
        red_saturation_slider.grid(row=4, column=1)

        #Green Saturation Slider
        green_saturation_factor = DoubleVar()
        green_saturation_factor.set(100)
        green_saturation_label = Label(self.frame3, text="Green Saturation:", bg="#1e1e1e", fg="white", font=("monospace", 12))
        green_saturation_slider = CTkSlider(self.frame3, from_=0, to=255,number_of_steps=10,
                                                 variable=green_saturation_factor,
                                                 command=lambda x=green_saturation_factor.get(): self.on_slide( "green_saturation", x))
        green_saturation_label.grid(row=5, column=0, padx=(10, 0), pady=5, sticky='w')
        green_saturation_slider.grid(row=5, column=1)

        #Blue Saturation Slider
        blue_saturation_factor = DoubleVar()
        blue_saturation_factor.set(100)
        blue_saturation_label = Label(self.frame3, text="Blue Saturation:", bg="#1e1e1e", fg="white", font=("monospace", 12))
        blue_saturation_slider = CTkSlider(self.frame3, from_=0, to=200,
                                                variable=blue_saturation_factor,
                                                command=lambda x=blue_saturation_factor.get(): self.on_slide("blue_saturation", x))
        blue_saturation_label.grid(row=6, column=0, padx=(10, 0), pady=5, sticky='w')
        blue_saturation_slider.grid(row=6, column=1)

        #contrast slider
        contrast_intensity = DoubleVar()
        contrast_intensity.set(0)
        contrast_label = Label(self.frame3, text="Contrast:", bg="#1e1e1e", fg="white",font=("monospace", 12))
        contrast_slider = CTkSlider(self.frame3, from_=-50, to=50, number_of_steps=10,
                                       variable=contrast_intensity,
                                       command=lambda x=contrast_intensity.get(): self.on_slide("contrast", x) if x==int(x) else None)
        contrast_label.grid(row=7, column=0, padx=(10, 0), pady=5, sticky='w')
        contrast_slider.grid(row=7, column=1)


        ################################################################
        #####################   CTK_SWITCHS   ##########################
        ################################################################

        #Edge Detection Switch
        edge_detect_var=BooleanVar()
        edge_detect=CTkSwitch(self.frame2,text="Edge detect", 
                              variable=edge_detect_var, 
                              command=lambda: self.on_click(("edge_detect",),edge_detect_var),
                              font=("monospace", 14))
        edge_detect.grid(row=0,column=1,padx=10,pady=10)

        #Sharpening Switch
        sharpen_var=BooleanVar()
        sharpen=CTkSwitch(self.frame2,text="Sharpen", 
                          variable=sharpen_var, 
                          command=lambda: self.on_click(("sharpen",),sharpen_var),
                          font=("monospace", 14))
        sharpen.grid(row=0,column=2,padx=10,pady=10)

        #Grayscaling Switch
        grayscale_var=BooleanVar()
        grayscale=CTkSwitch(self.frame2,text="Grayscale", 
                            variable=grayscale_var, 
                            command=lambda: self.on_click(("grayscale",),grayscale_var),
                            font=("monospace", 14))
        grayscale.grid(row=0,column=3,padx=10,pady=10)

        #Embossing Switch
        emboss_var=BooleanVar()
        emboss=CTkSwitch(self.frame2,text="Emboss", 
                         variable=emboss_var, 
                         command=lambda: self.on_click(("emboss",),emboss_var),
                         font=("monospace", 14))
        emboss.grid(row=0,column=4,padx=10,pady=10)

        #Negative Switch
        negative_var=BooleanVar()
        negative=CTkSwitch(self.frame2,text="Negative", 
                           variable=negative_var, 
                           command=lambda: self.on_click(("negative",),negative_var),
                           font=("monospace", 14))
        negative.grid(row=0,column=5,padx=10,pady=10)


        ################################################################
        #####################   RESIZE_ENTRY   #########################
        ################################################################

        resize_entry = Label(self.frame3, text="Resize: ", bg="#1e1e1e", fg="white", font=("monospace", 12))
        resize_entry.grid(row=8,column=0,padx=(10, 0), pady=10, sticky='w')

        Label(self.frame3,text="New width: ", bg="#1e1e1e", fg="white", font=("monospace", 10)).grid(row=9,column=0, padx=40, sticky="w")
        self.resize_width = Entry(self.frame3)
        self.resize_width.insert(0, "Width")
        self.resize_width.grid(row=9,column=1, pady=5)

        Label(self.frame3, text="New height: ", bg="#1e1e1e", fg="white", font=("monospace", 10)).grid(row=10,column=0, padx=40, sticky="w")
        self.resize_height = Entry(self.frame3)
        self.resize_height.insert(0, "Height")
        self.resize_height.grid(row=10,column=1, pady=5)

        submit_buttom= Button(self.frame3, 
                              text="Submit", bg="#383838", fg="white", 
                              borderwidth=0, activebackground="gray", width=10, height=1,
                              command=lambda: self.on_click(("resize",self.get_values()), variable),
                              font=("monospace", 10))
        submit_buttom.grid(row=11,column=1, pady=5)


    ################################################################
    #####################      METHODS     #########################
    ################################################################
    

    def get_values(self):
        return (int(self.resize_width.get()), int(self.resize_height.get()))

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
            self.im = ImageProcessor(self.filename)
            self.im.path = self.filename
            if self.im is not None:
                if self.lbl: self.lbl.destroy()
                self.lbl = Label(self.frame1, image=self.im.image.photoimage, bg="#1e1e1e")
                self.lbl.image = self.im.image.photoimage
                self.lbl.place(relx=0.5, rely=0.5, anchor="center")
        else:

            print("No image selected")


    def update_image(self, photoimage):
        if self.lbl:
            self.lbl.config(image=photoimage)
            self.im.image.photoimage = photoimage
        else:
            print("No label found")
