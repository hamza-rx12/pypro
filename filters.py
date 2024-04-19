import numpy as np
import cv2

class filters: 
    filterList=[]

    def __init__(self,image):
        self.image=image
    
    def applyFilter(self,filter):

        self.filterList.append(filter)
        for fil in self.filterList:

        

    def revokeFilter(self, filter):
        if filter in self.filterList:
            self.filterList.remove(filter)
            
        for fil in self.filterList:
            pass

        
