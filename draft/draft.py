import cv2
import numpy as np
from PIL import Image, ImageEnhance

# Charger l'image
image_path = "/home/ahmed/Bureau/Projet/OpenCV/images/carrefour2.jpeg"
image = cv2.imread(image_path)

# Vérifier si l'image est chargée correctement
if image is None:
    raise FileNotFoundError(f"L'image {image_path} n'a pas été trouvée.")

# Convertir en RGB (OpenCV charge en BGR)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Améliorer la netteté avec PIL
pil_image = Image.fromarray(image)
enhancer = ImageEnhance.Sharpness(pil_image)
sharpened_image = enhancer.enhance(2.0)  # Augmenter la netteté

# Convertir en tableau NumPy pour OpenCV
sharpened_image = np.array(sharpened_image)

# Convertir en niveaux de gris pour la détection des bords
gray = cv2.cvtColor(sharpened_image, cv2.COLOR_RGB2GRAY)
blurred = cv2.GaussianBlur(gray, (21, 21), 0)
edges = cv2.Canny(blurred, 50, 150)

# Créer un masque en dilatant les contours
kernel = np.ones((5,5), np.uint8)
mask = cv2.dilate(edges, kernel, iterations=3)
mask = cv2.GaussianBlur(mask, (21, 21), 0)

# Inverser le masque pour flouter l’arrière-plan
mask_inv = cv2.bitwise_not(mask)

# Appliquer un flou gaussien sur l'image entière
blurred_image = cv2.GaussianBlur(sharpened_image, (21, 21), 30)

# Appliquer le masque correctement pour garder l'avant-plan net
mask_inv = mask_inv / 255  # Normalisation entre 0 et 1
mask_inv = np.expand_dims(mask_inv, axis=-1)  # Adapter la dimension pour le broadcasting
final_image = (sharpened_image * mask_inv + blurred_image * (1 - mask_inv)).astype(np.uint8)

# Convertir en Image PIL et enregistrer
final_pil = Image.fromarray(final_image)
output_path = "carrefour2_processed.jpeg"
final_pil.save(output_path)

# Convertir l'image PIL en NumPy pour affichage OpenCV
final_cv = np.array(final_pil)
# final_cv = cv2.cvtColor(final_cv, cv2.COLOR_RGB2BGR)  # Repasser en BGR pour OpenCV

# Affichage avec OpenCV
# cv2.imshow("Image Traitée", final_cv)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

print(f"Image traitée et enregistrée : {output_path}")
