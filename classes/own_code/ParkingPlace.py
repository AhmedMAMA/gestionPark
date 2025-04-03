import cv2
import numpy as np
import matplotlib.pyplot as plt

class ParkingPlace:
    park_dir = "/home/ahmed/Desktop/Projet/OpenCV/images/park/"
    def __init__(self, image_path):
        self.image = cv2.imread( self.park_dir + image_path)
        if self.image is None:
            raise FileNotFoundError(f"L'image '{image_path}' est introuvable ou illisible.")
        self.handic = 0
        self.nohand = 0

    def ParkingField(self):
        img_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)  # Conversion en niveau de gris
        blur_img = cv2.GaussianBlur(img_gray, (5, 5), 0)  # Réduction du bruit
        bord_img = cv2.Canny(blur_img, 50, 150)  # Détection des contours

        # Détection des lignes
        line_img = cv2.HoughLinesP(bord_img, 1, np.pi/180, 50, minLineLength=150, maxLineGap=30)

        if line_img is not None:
            for line in line_img:
                x1, y1, x2, y2 = line[0]
                cv2.line(self.image, (x1, y1), (x2, y2), (0,255, 0), 2)  # Tracé des lignes en vert
        return line_img
    
    def axe2Rangement(self,lines_detected):
        lines_choice = []
        x_count = sum(1 for line in lines_detected if line[0][0] == line[0][2])  # Lignes verticales
        y_count = sum(1 for line in lines_detected if line[0][1] == line[0][3])  # Lignes horizontales
        if  x_count > y_count:
            for line in lines_detected:
                x1,y1,x2,y2 = line[0]
                if x1  == x2:
                    lines_choice.append((x1,y1,x2,y2))
            # Trier les lignes détectées par leur position X
            lines_choice.sort(key=lambda l: l[0])
        elif x_count < y_count:
            for line in lines_detected:
                x1,y1,x2,y2 = line[0]
                if y1  == y2:
                    lines_choice.append((x1,y1,x2,y2))
            # Trier les lignes détectées par leur position X
            lines_choice.sort(key=lambda l: l[1])

        return lines_choice

    def detectePlace(self,lines_detected):
        """_summary_

        Args:
            lines_detected (_type_): _description_
        """
        # Filtrer les lignes pour éviter les doublons
        unique_lines = []
        for (x1,y1,x2,y2) in lines_detected:
            if abs(x1 -  x2) > 150: # Seuil pour considérer une nouvelle ligne
                unique_lines.append((x1,y1,x2,y2))

        # Nombre de places = espaces entre les lignes
        print(f"Nombre de places détectées : {len(unique_lines) - 1}")
        return len(unique_lines) - 1

def mainFullPlace(img):
    rem = ParkingPlace(img)
    result = rem.ParkingField()  # Détecte les lignes

    if result is not None:  # Vérifie si des lignes ont été détectées
        lines = rem.axe2Rangement(result)  # Passe la liste des lignes détectées
        return rem.detectePlace(lines)  # Détecte les places de parking
    return None
