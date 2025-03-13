#Bibliothèque Require
import cv2
import easyocr
import numpy as np
import os
# from draft.draft import kernel
# from draft.main import reader
reader = easyocr.Reader(['fr', 'en'])  # Initialiser EasyOCR une seule fois
class ReconnaissanceTexte:

    reader = easyocr.Reader(['fr', 'en'])  # Initialiser EasyOCR une seule fois

    def __init__(self,image,name="",horaire="",place="",address="",id=""):
        self.name= name
        self.horaire = horaire
        self.address = address
        self.id = id
        self.image =  cv2.imread(image)
        if self.image is None:
            print(f"⚠️ Erreur : Impossible de charger l'image '{image}'. Vérifiez le chemin.")


    def zoneDeTexte(self):
        """_summary_
        Returns:
            np.array: Tableau 2D contenant les coordonnées des zones de texte détectées.
                - Ligne 0 : Coordonnées X des sommets des rectangles.
                - Ligne 1 : Coordonnées Y des sommets des rectangles.
        """
        if self.image is None:
            print(f"⚠️ Erreur : Impossible de charger l'image '{self.image}'. Vérifiez le chemin.")
            return None

        results = self.reader.readtext(self.image)

        # Stockage des coordonnées des rectangles détectés
        coord_rectangles = {'x': [], 'y': []}

        for bbox, text, score in results:
            coord_rectangles['x'].extend([int(point[0]) for point in bbox])
            coord_rectangles['y'].extend([int(point[1]) for point in bbox])

        return np.array([coord_rectangles['x'], coord_rectangles['y']])
    
    def textParZone(self):
        """_summary_
        Returns:
            list: Liste des périmètres définis par les coordonnées min/max en X et Y de chaque zone de texte sous forme de rectangle.
        """

        zone = self.zoneDeTexte()
        if zone is None:
            print("⚠️ Aucune zone de texte détectée !")
            return []
        x_coords, y_coords = zone[0],zone[1]
        nbre_zone = zone.shape[1] // 4 # Representant les rectangles définissant nos zone de texte

        x_rect = x_coords.reshape(nbre_zone, 4)
        y_rect = y_coords.reshape(nbre_zone, 4)

        # Création des rectangles
        rectangles = [[(int(x_rect[i, j]), int(y_rect[i, j])) for j in range(4)] for i in range(nbre_zone)]

        perimetres = []

        for rect in rectangles:
            x_values = [x for x, y in rect]
            y_values = [y for x, y in rect]

            # Ajout du périmètre sous forme ((minX, maxX), (minY, maxY))
            perimetres.append(((min(x_values), max(x_values)), (min(y_values), max(y_values))))
        
        print(f'Nos texte sont contenu dans les zone suivant : {perimetres}')
        return perimetres
    
    # Connaissance des caractères sur l'images via la ou les zone(s) de texte trouvées
    def reconnaissanceCaractère(self):
        for ((min_x,max_x),(min_y,max_y)) in self.textParZone():
            # new_image = self.image[min_y:max_y,min_x:max_x]
            new_image = self.pretraitement_image()[min_y:max_y, min_x:max_x]
            if new_image.size == 0:
                print(f'⚠️ Erreur : Imposition d\'extraire la zone de texte de l\'image originale')
                return
            # new_image = cv2.adaptiveThreshold(cv2.cvtColor(new_image,cv2.COLOR_BGR2GRAY),255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,5)

            # Détection des contour
            contours, _ = cv2.findContours(new_image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            for c in contours:
                M = cv2.moments(c)
                if M["m00"] == 0 :# cela correspond à l'aire de la zone
                    # print("Aucun éléments trouvés \n")
                    continue
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                # print(f'cX contient : {cX}  cY contient : {cY} \n\n')
            
            detectText = self.reader.readtext(new_image)

            for bbox, text, score in detectText:
                self.name += text + " "

        
            # Dessiner les annotations sur l'image originale
            cv2.rectangle(self.image, (min_x,min_y), (max_x,max_y), (0, 255, 0), 2)
            cv2.circle(self.image, (cX, cY), 5, (255, 0, 0), -1)
            cv2.imwrite("treate.png",new_image)
            print(f'L\'image contient : \n\n {self.name} \n\n')
    
    def pretraitement_image(self):
        """Appliquer des améliorations sur l'image avant OCR"""
        if self.image is None:
            print("⚠️ Erreur : Image introuvable.")
            return None

        # Convertir en niveaux de gris
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # Augmenter le contraste
        gray = cv2.equalizeHist(gray)

        # Appliquer un flou pour réduire le bruit
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # Appliquer un seuillage adaptatif plus doux
        thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

        return thresh


def GPT(path):
    # Read the image
    img_open = cv2.imread(f'/home/ahmed/Bureau/Projet/OpenCV/images/{path}')  
    if img_open is None:
        print("Error: Image not found or unable to load.")
        return

    # Convert to grayscale
    gray = cv2.cvtColor(img_open, cv2.COLOR_BGR2GRAY)

    # Apply threshold to binarize the image
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # cv2.imwrite("GPT.png",thresh)

    # Run OCR on the image
    reader = easyocr.Reader(['fr', 'en'])
    result = reader.readtext(thresh)

    # print(f'OCR Results for {path}: {result}')
    return result

num =  0
# Mieux 
def traitementProfond(result_gpt_EASYOCR_ONLY,path,function):
    global num
    num += 1
    # print(f'result_gpt_EASYOCR_ONLY : {result_gpt_EASYOCR_ONLY}')
    if result_gpt_EASYOCR_ONLY == []:
        print("Il n'y a pas de texte dans votre élément")
        return
    print(f"==========================DEBUT=======================================\t{function}")
    x_cord , y_cord = [],[]
    # print(f"result_gpt_EASYOCR_ONLY ======== {result_gpt_EASYOCR_ONLY}")

    for i,(bbox, text, score) in enumerate(result_gpt_EASYOCR_ONLY):
        # Extraction des coordonnées du rectangle englobant
        min_x, min_y = int(bbox[0][0]), int(bbox[0][1])
        max_x, max_y = int(bbox[2][0]), int(bbox[2][1])

        # Ajout des coordonnées dans les variables pour obtenir la zone à découper
        x_cord.extend([min_x, max_x])
        y_cord.extend([min_y, max_y])
        print(f'text initial : {text} | score : {score}')

    # Calcul des coordonnées minimales et maximales de la zone à découper
    min_x, max_x = min(x_cord), max(x_cord)
    min_y, max_y = min(y_cord), max(y_cord)


    img = cv2.imread(f'/home/ahmed/Bureau/Projet/OpenCV/images/{path}')
    zone_de_test = cv2.cvtColor(img[min_y:max_y,min_x:max_x],cv2.COLOR_BGR2GRAY)

    # Définition du chemin de sauvegarde
    save_dir = f"/home/ahmed/Bureau/Projet/OpenCV/search/"
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, f"{path}_zone_de_test_{function}_{num}.png")

    # Sauvegarde de l'image extraite
    cv2.imwrite(save_path, zone_de_test)

    print("Image Sauvegarder à lire")
    results = reader.readtext(save_path)
    print(f'Source traitée : {save_path}')
    for bbox,text,score in results:
        print(f'text trouvé = {text} | score  = {score}')



    ## LES CONTOURS
    contours, _ = cv2.findContours(zone_de_test,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        M = cv2.moments(contour)
        c_x = int( M["m10"] / M["m00"] )
        c_y = int( M["m01"] / M["m00"])
        # print(f'x : {x} | y : {y} | w : {w} | h : {h} |  M["m10"] = {M["m10"]} |  M["m00"] : {M["m00"]} | M["m01"] = {M["m01"]}" | c_x : {c_x} | c_y = {c_y}')
    ##
    # = cv2.imread(path)
    # print(f'x_cords : {x_cord}, \n y_cord : {y_cord}')

# Mieux que GPT
def GPT1(path):
    global num
    num +=  1
    # Read the image
    img_open = cv2.imread(f'/home/ahmed/Bureau/Projet/OpenCV/images/{path}')  
    if img_open is None:
        print("Error: Image not found or unable to load.")
        return

    # Convert to grayscale
    gray = cv2.cvtColor(img_open, cv2.COLOR_BGR2GRAY)

    # Apply threshold to binarize the image
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    # Utiliser des opérations morphologiques pour améliorer les contours
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dilated = cv2.dilate(thresh, kernel, iterations=1)  # Dilatation pour renforcer les contours
    ret = cv2.imwrite(f"{path}_{num}.png",dilated)
    if ret:
        print("Image sauvegarder")

    # cv2.imwrite("GPT.png",thresh)

    # Run OCR on the image
    reader = easyocr.Reader(['fr', 'en'])
    result = reader.readtext(dilated)

    # print(f'OCR Results for {path}: {result}')
    return result


def traitementProfond1(result_gpt_EASYOCR_ONLY,path,function):
    global num
    num += 1
    # print(f'result_gpt_EASYOCR_ONLY : {result_gpt_EASYOCR_ONLY}')
    if result_gpt_EASYOCR_ONLY == []:
        print("Il n'y a pas de texte dans votre élément")
        return
    print(f"==========================DEBUT=======================================\t{function}")
    x_cord , y_cord = [],[]
    # print(f"result_gpt_EASYOCR_ONLY ======== {result_gpt_EASYOCR_ONLY}")

    for bbox, text, score in result_gpt_EASYOCR_ONLY:
        # Extraction des coordonnées du rectangle englobant
        min_x, min_y = int(bbox[0][0]), int(bbox[0][1])
        max_x, max_y = int(bbox[2][0]), int(bbox[2][1])

        # Ajout des coordonnées dans les variables pour obtenir la zone à découper
        x_cord.extend([min_x, max_x])
        y_cord.extend([min_y, max_y])
        print(f'text initial : {text} | score : {score}')

    # Calcul des coordonnées minimales et maximales de la zone à découper
    min_x, max_x = min(x_cord), max(x_cord)
    min_y, max_y = min(y_cord), max(y_cord)


    img = cv2.imread(f'/home/ahmed/Bureau/Projet/OpenCV/images/{path}')
    zone_de_test = cv2.adaptiveThreshold(cv2.cvtColor(img[min_y:max_y,min_x:max_x],cv2.COLOR_BGR2GRAY),255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,23,5)

    # Définition du chemin de sauvegarde
    save_dir = f"/home/ahmed/Bureau/Projet/OpenCV/search/"
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, f"{path}_zone_de_test_{function}_{num}.png")

    # Sauvegarde de l'image extraite
    cv2.imwrite(save_path, zone_de_test)

    print("Image Sauvegarder à lire")
    results = reader.readtext(save_path)
    print(f'Source traitée : {save_path}')
    for bbox,text,score in results:
        print(f'text trouvé = {text} | score  = {score}')

