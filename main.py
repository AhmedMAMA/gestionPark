#Require
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from classes.own_code.ParkingPlace import mainFullPlace
from classes.own_code.YoloParking import mainManagePark
from classes.own_code.Structure import mainStructure
from web.server.config import DB

# #End Require


# Image à prédire
park0 = "park.jpg" # Parling Image
img = "carrefour.webp" # Banner of Agency

strcut =  mainStructure(img)
full_count = mainFullPlace(park0)
parki = mainManagePark(strcut,park0)

print(f'strcut : {strcut} full_count : {full_count} -  parki : {parki}') #DeBug code

#DataBase Connexion
conect = DB()
address = "123 Rue Exemple, Paris"  # Remplace cette valeur par l'adresse réelle
conect.sendData(strcut, address, full_count, parki['hand'], parki['vehicle'])
