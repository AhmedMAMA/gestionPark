from easyocr import Reader
from sys import exit
from cv2 import imread,cvtColor,threshold,getStructuringElement,dilate, THRESH_BINARY,COLOR_RGBA2GRAY,MORPH_RECT
# from serpapi import GoogleSearch

class Structure:

    # Mes variables d'environnement global
    path_dir = "/home/ahmed/Bureau/Projet/OpenCV/images/ensignes/"
    save_dir = "/home/ahmed/Bureau/Projet/OpenCV/vues/ensignes/"
    read_img =  Reader(['fr', 'en'])# Initialiser EasyOCR une seule fois

    def __init__(self,img):
        """Constructor of our POO CLass Structure

        Args:
            img (numpyArray): That is your image in array format. Which is the openCV format
        """
        self.img = imread(self.path_dir + img)
        if self.img is None:
            print(f"⚠️ Erreur : Impossible de charger l'image '{img}'. Vérifiez le chemin.")
            exit()

        self.tim = ""
        self.nam =""
        self.add = ""
        self.imT = img
    
    def readingF(self):
        """Find the bounding of the text present in the self image

        Returns:
            list: THe list that returns is the coordinate for point which maybe contain the letter
        """
        # Convert my picture to gray
        gray = cvtColor(self.img,COLOR_RGBA2GRAY)
        #Apply threshold to binarize the image
        _,thresh = threshold(gray,135,255,THRESH_BINARY)
        #Utiliser des opération morphologique pour améliorr les contour des textes
        kernel   = getStructuringElement(MORPH_RECT,(5,5))
        dilated  = dilate(thresh,kernel,iterations=1)

        box_tex = self.read_img.readtext(dilated)

        return box_tex
        
    def traitementProfond(self,box_text):
        """Function that retreat the section of picture where the program found the text.

        Args:
            box_text (list): contain all information about the section selected by the previous function
                            bbox : Which represente des coodination of the point that delimit the rectangle which contain the letter
                            text : Information taping contain in the rectangle
                            score: The performance about prediction (finding the good information : text)

        Returns:
            str: The function return the text that has a best score between all of treatement text in the image
        """
        if box_text is None:
            print(f'The image that provides don\'t contain any text')
            exit()
        
        print(f'='*32,'Starting Program')
        x_cord,y_cord = [],[]

        #collect the coodonnate of points in box_text
        for bbox,text,score in box_text:
            min_x, min_y = int(bbox[0][0]), int(bbox[0][1])
            max_x, max_y = int(bbox[2][0]), int(bbox[2][1])

            # Ajout des coordonnées dans les variables pour obtenir la zone à découper
            x_cord.extend([min_x, max_x])
            y_cord.extend([min_y, max_y])
            print(f'text initial : {text} | score : {score}')
        
        min_x,max_x = min(x_cord),max(x_cord)
        min_y,max_y = min(y_cord),max(y_cord)

        select_part = cvtColor(self.img[min_y:max_y,min_x:max_x],COLOR_RGBA2GRAY)

        # Read the new partial from the image that we have selected
        bounding_B = self.read_img.readtext(select_part)

        for  index, (bbox, text, score) in enumerate(bounding_B):
            # if box_text[index][2] < score:
            #     self.nam += text +" "
            # else: self.nam += box_text[index][1] +" "
            self.nam += text +" "
            print(f'The text found is {text} with accuracy {score}')
        
        return self.getName()
    
    # def timing(self):
    #     """The function show the information timing table about the agency found

    #     Returns:
    #         dict | json: List all information about the agency
    #     """
    #     params = {
    #         "engine": "google_maps",
    #         "q":  self.getName(), # That reline to the name of agency
    #         "ll": "@40.7455096,-74.0083012,14z", # That repesente de current positon for the user (it's changing)
    #         "api_key": "189f0e9a592c3d126f8c81f97b0371e37398ded078dee6f48aa3b85d4e4ecf9f" # This is my own API KEY from SERAPI GOOGLE (https://serpapi.com/users/auth/google_oauth2)
    #     }
    #     search = GoogleSearch(params)
    #     return search.get_dict()
    
    def getName(self): return self.nam
    def getAdd(self): return self.add
    def getTim(self): return self.tim
    def getTim(self): return self.imT


# Main Program
def mainStructure(img):
    strct = Structure(img)

    # print(f'traitementProfond : {strct.traitementProfond(strct.readingF())} ')
    
    return strct.traitementProfond(strct.readingF())





