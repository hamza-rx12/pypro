import image

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
            self.image=self.image.filter_choose(fil);