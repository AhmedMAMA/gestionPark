import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# #End Require

from classes.StructureCLasses import main

racine_auchan = "/home/ahmed/Bureau/Projet/OpenCV/images/auchan.webp"
racine_carrefour_jpeg = "/home/ahmed/Bureau/Projet/OpenCV/images/carrefour.jpeg"
racine_carrefour_webp = "/home/ahmed/Bureau/Projet/OpenCV/images/darty.jpg"

# print("ESSAI AVEC L'IMAGE AUCHAN.WEBP")
# main(racine_auchan)

# print("ESSAI AVEC L'IMAGE CARREFOUR.JPEG")
# main(racine_carrefour_jpeg)

print("ESSAI AVEC L'IMAGE DARTY")
main(racine_carrefour_webp)
