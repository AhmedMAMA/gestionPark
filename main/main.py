#Require
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# #End Require

from classes.reconnaissanceTexte import *
path = "auchan.webp"
# path1 = "carrefour.png"
path1= "carrefour.jpeg"
path3 = "carrefour.webp"

# # gestion.functionStand()
print("\n\n")
traitementProfond(GPT1(path),path,"GPT")

print("\n\n\n")
traitementProfond(GPT1(path1),path1,"GPT")

print("\n\n\n")
traitementProfond(GPT1(path3),path3,"GPT")


# FAIM10F