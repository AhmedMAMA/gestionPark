
# from libs.identify import*

import cv2
import numpy as np
import easyocr

def champDeTexte(img_path):
    """
    Identifie les zones contenant du texte dans une image en utilisant EasyOCR.

    Args:
        img_path (str): Chemin vers l'image à analyser.

    Returns:
        np.array: Tableau 2D contenant les coordonnées des zones de texte détectées.
                  - Ligne 0 : Coordonnées X des sommets des rectangles.
                  - Ligne 1 : Coordonnées Y des sommets des rectangles.

    Exemple :
        >>> champDeTexte("image.jpg")
        array([[380, 712, 714, 382, 458, 718, 722, 462],
               [215, 183, 276, 308, 299, 270, 374, 403]])
    """
    reader = easyocr.Reader(['fr', 'en'])
    result = reader.readtext(img_path)

    # Stockage des coordonnées des rectangles détectés
    coord_rectangles = {'x': [], 'y': []}

    for bbox, text, score in result:
        coord_rectangles['x'].extend([int(point[0]) for point in bbox])
        coord_rectangles['y'].extend([int(point[1]) for point in bbox])

    return np.array([coord_rectangles['x'], coord_rectangles['y']])


def treatImage(coordonnees_points):
    """
    Traite les coordonnées des sommets pour extraire les rectangles contenant du texte.

    Args:
        coordonnees_points (np.array): Tableau 2D contenant les coordonnées des points détectés.

    Returns:
        list: Liste des périmètres, chaque périmètre étant défini par deux paires de coordonnées.

    Exemple :
        >>> coordonnees = np.array([
        ...     [380, 712, 714, 382, 458, 718, 722, 462],
        ...     [215, 183, 276, 308, 299, 270, 374, 403]
        ... ])
        >>> treatImage(coordonnees)
        [[(380, 714), (183, 308)], [(458, 722), (270, 403)]]
    """
    x_coords = coordonnees_points[0]
    y_coords = coordonnees_points[1]

    nb_rectangles = coordonnees_points.shape[1] // 4  # Chaque rectangle a 4 sommets

    x_rect = x_coords.reshape(nb_rectangles, 4)
    y_rect = y_coords.reshape(nb_rectangles, 4)

    # Création des rectangles
    rectangles = [[(int(x_rect[i, j]), int(y_rect[i, j])) for j in range(4)] for i in range(nb_rectangles)]
    
    return perimetre(rectangles)


def perimetre(rectangles):
    """
    Délimite les champs de texte détectés dans l'image.

    Args:
        rectangles (list): Liste de rectangles représentés par 4 points (x, y).

    Returns:
        list: Liste des périmètres définis par les coordonnées min/max en X et Y.
    """
    perimetres = []

    for rect in rectangles:
        x_values = [x for x, y in rect]
        y_values = [y for x, y in rect]

        # Ajout du périmètre sous forme ((minX, maxX), (minY, maxY))
        perimetres.append(((min(x_values), max(x_values)), (min(y_values), max(y_values))))
    
    return perimetres


def main(pathImg):
    #Image dont il faut extrait le(s) texte(s)
    coordonnees_points  = champDeTexte(pathImg)
    print(treatImage(coordonnees_points))

"""
Fonction principale pour détecter et extraire le texte d'une image.
"""
# Charger l'image originale
path = "/home/ahmed/Bureau/Projet/OpenCV/images/auchan.webp"
# path = "/home/ahmed/Bureau/Projet/OpenCV/images/carrefour2.jpeg"
orig = cv2.imread(path)

if orig is None:
    print(f"⚠️ Erreur : Impossible de charger l'image '{path}'. Vérifiez le chemin.")
    
 # Détection des coordonnées des zones de texte
coordonnees_points = champDeTexte(path)
retraitement = treatImage(coordonnees_points)

reader = easyocr.Reader(['fr', 'en'])  # Initialiser EasyOCR une seule fois
content = ""

for i, img in enumerate(retraitement):
    x_min, x_max = img[0]
    y_min, y_max = img[1]

    # Vérification des limites de l'image
    if x_max > orig.shape[1] or y_max > orig.shape[0]:
        print(f"⚠️ Erreur : Les coordonnées dépassent les dimensions de l'image ({orig.shape[1]}, {orig.shape[0]}).")
        continue
        
    text_roi = orig[y_min:y_max, x_min:x_max]
    # Vérification si la région extraite est vide
    if text_roi.size == 0:
        print(f"⚠️ Aucune donnée extraite pour la zone {i}.")
        continue

    result = reader.readtext(text_roi)
    for bbox, text, score in result:
        content += text + " "
    # print(reader.readtextlang(text_roi))

    print(f"🔹 Texte détecté {i} : {text}")
    # Affichage de la région extraite
    text_roi_gray = cv2.cvtColor(text_roi, cv2.COLOR_BGR2GRAY)
    text_roi = cv2.adaptiveThreshold(text_roi_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,5)
    for i in range(text_roi.shape[0]):
        print(f"Ligne {i}: {text_roi[i]}")

    # print("text_roi\n",text_roi, "\n",text_roi.shape)
    # cv2.imshow(f'Texte {i}', text_roi)
    # cv2.waitKey(0)

# cv2.destroyAllWindows()
print("\n📜 Contenu extrait :")
print(content.strip())

# print("Seconde chance")
# result = reader.readtext(orig)
# for bbox,text,score in  result:
#     print(text)

# cv2.imshow(f'Texte {i}', orig)
# cv2.waitKey(0)

# cv2.destroyAllWindows()











# # Charger l'image
reader = easyocr.Reader(['fr', 'en'])

## Function de retraitement de l'image
for index, ((minX, maxX), (minY, maxY)) in enumerate(retraitement):
    # Vérification des coordonnées
    if minX >= maxX or minY >= maxY:
        print(f"⚠️ Erreur : Rectangle invalide ({minX}, {maxX}), ({minY}, {maxY})")
        continue

    # Extraire la région de texte
    text_roi = orig[minY:maxY, minX:maxX]

    if text_roi.size == 0:
        print(f"⚠️ Erreur : Zone extraite vide à l'index {index}")
        continue

    # print(f"Shape de text_roi : {text_roi.shape}")

    # Convertir en niveaux de gris et filtrer le bruit
    # gray =
    thresh = cv2.adaptiveThreshold(cv2.cvtColor(text_roi, cv2.COLOR_BGR2GRAY), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 5)

    # Afficher l'image en cours de traitement
    # cv2.imshow(f"Image {index}", thresh)
    # cv2.waitKey(0)

    # Détecter les contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    content = ""

    for c in contours:
        M = cv2.moments(c)
        if M["m00"] == 0:
            continue

        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

    # Utiliser EasyOCR pour lire le texte
    result = reader.readtext(text_roi)
    
    for bbox, text, score in result:
        content += text + " "

    # Dessiner les annotations sur l'image originale
    cv2.rectangle(orig, (minX, minY), (maxX, maxY), (0, 255, 0), 2)
    cv2.circle(orig, (cX, cY), 5, (255, 0, 0), -1)

    print(f'Texte trouvé1 : {content}')

    # Afficher l'image finale avec annotations
    # cv2.imshow("Texte détecté", orig)
    # cv2.waitKey(0)

# cv2.destroyAllWindows()
