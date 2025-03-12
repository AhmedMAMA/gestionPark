import cv2
import easyocr
import numpy as np  
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


# Charger l'image
path = "/home/ahmed/Bureau/Projet/OpenCV/images/auchan.webp"
orig = cv2.imread(path)

if orig is None:
    print(f"⚠️ Erreur : Impossible de charger l'image '{path}'. Vérifiez le chemin.")
    exit()

# Détection des zones de texte
coordonnees_points = champDeTexte(path)
retraitement = treatImage(coordonnees_points)

print(f"Coordonnées des rectangles détectés : {retraitement}")

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

    print(f"Shape de text_roi : {text_roi.shape}")

    # Convertir en niveaux de gris et filtrer le bruit
    gray = cv2.cvtColor(text_roi, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 5)

    # Afficher l'image en cours de traitement
    cv2.imshow(f"Image {index}", thresh)
    cv2.waitKey(0)

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

    print(f'Texte trouvé : {content}')

    # Afficher l'image finale avec annotations
    cv2.imshow("Texte détecté", orig)
    cv2.waitKey(0)

cv2.destroyAllWindows()
