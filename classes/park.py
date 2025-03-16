import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# #End Require

from classes.ParkingPlace import main
park1 = "/home/ahmed/Bureau/Projet/OpenCV/images/park.jpg"
park2 = "/home/ahmed/Bureau/Projet/OpenCV/images/park1.webp"
park3= "/home/ahmed/Bureau/Projet/OpenCV/images/parking.png"
main(park1)