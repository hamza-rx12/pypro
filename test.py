# import image
import imagemaster
# im = image.image("./src/free-images.jpg")
# im.blur()
# im.sharpen()
# print(im.)
# # im.show()
im=imagemaster.imageProcessor("./src/free-images.jpg")
im.applyFilter("blur")
# im.applyFilter("sharpen")
# im.applyFilter("negative")
# im.applyFilter("positive")
# im.applyFilter("sharpen")
print(im.filterList)
im.image.show()

