from Image import Image_


class ImageProcessor:
    def __init__(self,path):
        self.filterList=[]
        self.path=path
        self.image=Image_(path)


    def applyFilter(self,filter):
        filternames=list(map(lambda x: x[0],self.filterList))
        self.image=Image_(self.path)

        if filter[0] not in filternames:
            self.filterList.append(filter)
        else :
            self.filterList.pop(filternames.index(filter[0]))
            self.filterList.append(filter)
        for fil in self.filterList:
            self.image.filter_choose(fil)
        print(self.filterList)


    def revokeFilter(self, filter):
        self.image = Image_(self.path)

        if filter in self.filterList:
            self.filterList.remove(filter)
        else:
            print("Filter not found in the list.")

        for fil in self.filterList:
            self.image.filter_choose(fil)