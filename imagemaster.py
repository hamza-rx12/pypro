from GUI import *
from PIL import Image,ImageTk


def main():

    app=GUI()
    icon_image = Image.open('./src/Imagemaster.png')
    icon_photo = ImageTk.PhotoImage(icon_image)
    app.iconphoto(True, icon_photo)
    app.mainloop()


if __name__ == "__main__":
    main()















