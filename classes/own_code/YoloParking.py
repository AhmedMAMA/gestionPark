# from classes.own_code.Structure import Structure
from ultralytics import YOLO

class YoloParking:
    yolo_dir = "/home/ahmed/Desktop/Projet/OpenCV/classes/model/best.pt"
    park_dir = "/home/ahmed/Desktop/Projet/OpenCV/images/park/"
    def __init__(self,struct,park):
      self.strt =  struct # Qui correspond à toutes les informations de la structure found
      self.park = self.park_dir + park # Image ou vidéo de park

    
    def getHand(self): return self.hand
    def getVehicle(self): return self.hand

    def predict(self):
        """This function make predict to find how many 

        Returns:
            _type_: _description_
        """
        model = YOLO(self.yolo_dir) # Mon model YOLO
        # Prédict
        predt = model.predict(self.park)
        # Colllect  data predicted
        dataP = predt[0]

        # Collect all of classes & accurancy
        clasN = dataP.boxes.cls
        # score = dataP.boxes.conf

        # The names classses that I'm using
        namCl = {0:'hand',1:'vehicle'}

        # Counter for each class name
        count = {name : 0 for name in namCl.values()} # initiation
        for cls in clasN:
            class_name = namCl[int(cls)]
            count[class_name] += 1
        return count
    
def mainManagePark(struct,park):
    # struct = mainStructure() # Structure Name found
    parkMa = YoloParking(struct,park)
    return parkMa.predict()
