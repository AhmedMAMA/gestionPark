#Bibliothèque Require
import cv2
import easyocr
import numpy as np
import os
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









# def EASYOCR_ONLY(path):

#     # Read the image
#     img_open = cv2.imread(f'/home/ahmed/Bureau/Projet/OpenCV/images/{path}')  
#     if img_open is None:
#         print("Error: Image not found or unable to load.")
#         return

#     # Convert to grayscale (to ensure it's CV_8UC1)
#     gray = cv2.GaussianBlur(cv2.cvtColor(img_open, cv2.COLOR_BGR2GRAY),(5,5),0)

#     # Apply threshold to convert it to binary (black & white)
#     thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,13,4)
#     # cv2.imwrite("EASYOCR_ONLY.png",thresh)
#     reader = easyocr.Reader(['fr', 'en'])
#     result = reader.readtext(thresh)
#     print(f'OCR Results for {path}: {result}')
#     return result



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
def traitementProfond(result_gpt_EASYOCR_ONLY,path,function):
    global num
    num += 1
    print(f'result_gpt_EASYOCR_ONLY : {result_gpt_EASYOCR_ONLY}')
    if result_gpt_EASYOCR_ONLY == []:
        print("Il n'y a pas de texte dans votre élément")
        return
    print(f"==========================DEBUT=======================================\t{function}")
    x_cord , y_cord = [],[]
    for bbox, text,score in result_gpt_EASYOCR_ONLY:
        print(f'Texte initial : {text} | Score initial : {score}')
        # Extraction des coordonnées (conversion explicite en int si nécessaire)
        x_cord.extend(int(point[0]) for point in bbox)
        y_cord.extend(int(point[1]) for point in bbox)
    
    min_x,max_x = min(x_cord),max(x_cord)
    
    min_y,max_y = min(y_cord),max(y_cord)

    img = cv2.imread(f'/home/ahmed/Bureau/Projet/OpenCV/images/{path}')
    zone_de_test = cv2.cvtColor(img[min_y:max_y,min_x:max_x],cv2.COLOR_BGR2GRAY)
    ## AJOUT NOUVEL ##
    # zone_de_test = cv2.adaptiveThreshold(cv2.GaussianBlur(zone_de_test,(7,7),0),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,5)
    # _,zone_de_test = cv2.threshold(zone_de_test, 127, 255, cv2.THRESH_BINARY)
    ## AJOUT NOUVEL ##
    # Définition du chemin de sauvegarde
    save_dir = f"/home/ahmed/Bureau/Projet/OpenCV/search/{function}/"
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, f"{path}_zone_de_test{function}{num}.png")

    # Sauvegarde de l'image extraite
    cv2.imwrite(save_path, zone_de_test)

    print("Image Sauvegarder à lire")
    results = reader.readtext(save_path)
    
    for bbox,text,score in results:
        print(f'text trouvé = {text} | score  = {score}')



    ## LES CONTOURS
    contours, _ = cv2.findContours(zone_de_test,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        M = cv2.moments(contour)
        if M["m00"] == 0:
            continue
        c_x = int( M["m10"] / M["m00"] )
        c_y = int( M["m01"] / M["m00"])



def traitementProfond2(result_gpt_EASYOCR_ONLY, path, function):
    x_cord, y_cord = [], []

    # Extraction des coordonnées des bounding boxes détectées par EasyOCR
    for bbox, text, score in result_gpt_EASYOCR_ONLY:
        print(f'BBox : {bbox}, Texte détecté : {text}')
        x_cord.extend(int(point[0]) for point in bbox)
        y_cord.extend(int(point[1]) for point in bbox)

    min_x, max_x = min(x_cord), max(x_cord)
    min_y, max_y = min(y_cord), max(y_cord)

    img = cv2.imread(f'/home/ahmed/Bureau/Projet/OpenCV/images/{path}')
    zone_de_test = img[min_y:max_y, min_x:max_x]
    gray = cv2.cvtColor(zone_de_test, cv2.COLOR_BGR2GRAY)

    # Appliquer un seuillage pour binariser l'image
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

    # Définition du chemin de sauvegarde
    save_dir = "/home/ahmed/Bureau/Projet/OpenCV/search"
    os.makedirs(save_dir, exist_ok=True)
    # save_path = os.path.join(save_dir, f"{path}_zone_de_test_{function}.png")

    # # Sauvegarde de l'image extraite
    # cv2.imwrite(save_path, thresh)

    ## Détection des contours pour extraire les caractères un par un
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Liste pour stocker les caractères avec leurs positions
    char_data = []

    print("\n=== Caractères détectés ===")

    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)

        # Filtrer les petits bruits
        if w < 5 or h < 5:
            continue

        # Calculer le centre de masse (c_x, c_y)
        M = cv2.moments(contour)
        if M["m00"] != 0:  # Éviter la division par zéro
            c_x = int(M["m10"] / M["m00"])
            c_y = int(M["m01"] / M["m00"])
        else:
            c_x, c_y = x + w // 2, y + h // 2  # Approximation si M["m00"] = 0

        # Ajouter les infos du caractère à la liste
        char_data.append((x, y, c_x, c_y, w, h, contour))

    # Trier les caractères par leur position en X (de gauche à droite)
    char_data.sort(key=lambda char: char[2])

    # OCR sur chaque caractère
    reader = easyocr.Reader(['fr', 'en'])

    for i, (x, y, c_x, c_y, w, h, contour) in enumerate(char_data):
        # Extraire le caractère
        char_roi = gray[y:y+h, x:x+w]

        # Sauvegarder l’image du caractère
        char_save_path = os.path.join(save_dir, f"{path}_char_{i}.png")
        cv2.imwrite(char_save_path, char_roi)

        # Appliquer OCR sur chaque caractère
        result_text = reader.readtext(char_roi, detail=0)  # detail=0 pour récupérer uniquement le texte

        # Afficher le texte détecté avec ses coordonnées
        print(f"Caractère {i} : {result_text} | Centre : ({c_x}, {c_y})")

        # Dessiner le contour et le centre du caractère sur l'image d'origine
        cv2.rectangle(zone_de_test, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(zone_de_test, (c_x, c_y), 3, (255, 0, 0), -1)  # Point bleu pour centre

    # Sauvegarde de l'image annotée avec les caractères
    cv2.imwrite(os.path.join(save_dir, f"{path}_zone_de_test_annotated.png"), zone_de_test)

    print("=== Fin de l'extraction des caractères ===")
