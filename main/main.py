#Require
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

#End Require

from classes.reconnaissanceTexte import *
path = "auchan.webp"
# path1 = "carrefour.png"
path2 = "carrefour.jpeg"
path3 = "carrefour.webp"
# gestion = ReconnaissanceTexte(path) # Pas performant
# gestion.reconnaissanceCaractère()

# gestion.functionStand()
print("\n POUR - AUCHANn\n==========================================================\n")
# traitementProfond(EASYOCR_ONLY(path),path,"EASYOCR_ONLY")
traitementProfond(GPT(path),path,"GPT")

# print("\n\n\n Carrefour")
# traitementProfond(EASYOCR_ONLY(path1),path1,"EASYOCR_ONLY")
# traitementProfond(GPT(path1),path1,"GPT")

print("\n\n\n Carrefour2")
# traitementProfond(EASYOCR_ONLY(path2),path2,"EASYOCR_ONLY")
traitementProfond(GPT(path2),path2,"GPT")

print("\n\n\n Carrefour2")
# traitementProfond(EASYOCR_ONLY(path2),path2,"EASYOCR_ONLY")
traitementProfond(GPT(path3),path3,"GPT")