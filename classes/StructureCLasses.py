import easyocr
import cv2
# from serpapi import GoogleSearch
# from classes.reconnaissanceTexte import reader

class StructureCLasses:
    # Initiateur de lecture de texte sur image
    reader = easyocr.Reader(['fr', 'en'])
    # Fonction d'initialisation de la classe
    def __init__(self,image):
        """_summary_

        Args:
            image (_type_): _description_
        """
        self.imag = image
        self.name = ''
        self.when = ''
        self.address = ''
        if self.imag is None:
            print(f"⚠️ Erreur : Impossible de charger l'image '{image}'. Vérifiez le chemin.")


    def zone2Text(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        img_open = cv2.imread(self.imag)
        if img_open is None:
            print(f"⚠️ Erreur : Impossible de charger l'image '{self.imag}'. Vérifiez le chemin.")
            return
        img_gray = cv2.cvtColor(img_open,cv2.COLOR_BGR2GRAY)
        _,thresh = cv2.threshold(img_gray,127,255,cv2.THRESH_BINARY)
        kernel   = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
        dilate   = cv2.dilate(thresh,kernel,iterations=1)
        result = self.reader.readtext(dilate)
        return result
    
    def traitement2Image(self,result):
        print(f'image : {self.imag}')
        """_summary_

        Args:
            result (_type_): _description_

        Returns:
            _type_: _description_
        """
        if not result:
            print(f'Il n\'y a rien dans les données collectées lors de détection de la zone de texte ')
            return
        text_score = []
        x_cords,y_cords = [],[]
        for bbox,text,score in result:
            min_x,min_y = int( bbox[0][0] ), int( bbox[0][1] )
            max_x,max_y = int( bbox[2][0] ),int( bbox[2][1] )
            x_cords.extend([min_x,max_x])
            y_cords.extend([min_y,max_y])
            text_score.append((text,score))

        min_x,max_x =  min(x_cords),max(x_cords)
        min_y,max_y =  min(y_cords),max(y_cords)

        img_opening = cv2.imread(self.imag)
        img_treated = cv2.cvtColor(img_opening[min_y:max_y,min_x:max_x],cv2.COLOR_BGR2GRAY)

        # Traçabilité du programme ou image à relire
        print(f'La nouvelle image a traité; sera sauvegardée dans le dossier vue')
        cv2.imwrite(f'traitement2Image.png',img_treated)
        #Text contenu dans l'image
        text_Find =""
        
        #Relecture de la zone de texte trouvée
        in_the_imag = self.reader.readtext(img_treated)
        for index,(bbox, text,  score) in enumerate(in_the_imag):
            print(f'[1] - Sur l\'ancien  inmage on a: text = {text_score[index][0]} | Score : {text_score[index][1]}. \n[2] - Sur la nouvelle image on a : text : {text} | score : {score}')
            if score >= text_score[index][1]: text_Find += text + " "
            else: text_Find += text_score[index][0] + " "        
        return text_Find
    
    def when_open(company):
        """_summary_
        Args:
            company (str): Represente le nom de la structure trouver sur l'image
        Returns:
            list: Représente un json des informations liées à l'enttreprise ( type, name, adresses, horaires,....)
        """
        print(f'Informations collectées sur {company}')
        params = {
        "engine": "google_maps",
        "q": company,
        "ll": "@40.7455096,-74.0083012,14z",
        "api_key": "189f0e9a592c3d126f8c81f97b0371e37398ded078dee6f48aa3b85d4e4ecf9f"
        }
        # search = GoogleSearch(params)
        # results = search.get_dict()
        # return results
    
    def saveData(self,opening):
        """_summary_

        Args:
            opening (arrray): détient toutes les informations sur l'entreprise( type, name,addresse,  horaire,......)
        """
        if "local_results" in opening:
            for place in opening["local_results"]:
                self.name = place.get("title", "Nom inconnu")
                self.address = place.get("address", "Adresse inconnue")
                self.when = place.get("hours", "Horaires non disponibles")

                print(f"🏢 Nom : {self.name}")
                print(f"📍 Adresse : {self.address}")
                print(f"⏰ Horaires : {self.when}")
                print("-" * 50)
        else:
            print("Aucun résultat trouvé.")


#Fonction principal    
def main(path_imag):
    print("Notre fonction principale")
    structureClasse = StructureCLasses(path_imag)
    result = structureClasse.zone2Text()
    text_find = structureClasse.traitement2Image(result)
    
    print(f'TEXT FOUND : {text_find}')
    # print("structureClasse.when_open(text_find) : ",structureClasse.when_open(text_find))
## Données reçu pour Auchan via google collab
