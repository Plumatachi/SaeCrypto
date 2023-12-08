from PIL import Image

def bmp_to_tuples(image_path):
    # Ouvrir l'image BMP
    img = Image.open(image_path)

     # Convertir l'image en mode "RGB" si elle n'est pas déjà en mode "RGB"
    if img.mode != "RGB":
        img = img.convert("RGB")

    # Obtenir les dimensions de l'image
    largeur, hauteur = img.size

    # Initialiser une liste pour stocker les tuples (Rouge, Vert, Bleu)
    liste_tuples = []

    # Parcourir chaque pixel de l'image
    for y in range(hauteur):
        for x in range(largeur):
            # Obtenir la couleur du pixel
            couleur_pixel = img.getpixel((x, y))

            # Ajouter le tuple à la liste
            liste_tuples.append(couleur_pixel)

    return liste_tuples

# Chemin de l'image BMP
chemin_image_bmp = "rossignol1.bmp"
chemin_image_bmp2 = "rossignol2.bmp"

# Appeler la fonction et obtenir la liste de tuples
liste_couleurs = bmp_to_tuples(chemin_image_bmp)
liste_couleurs2 = bmp_to_tuples(chemin_image_bmp2)

from PIL import Image

def extract_key_from_bmp(image_path):
    # Ouvrir l'image BMP avec Pillow
    img = Image.open(image_path)

    # Récupérer les dimensions de l'image
    largeur, hauteur = img.size

    # Initialiser la clé binaire
    key_binary = ""

    # Parcourir l'image pixel par pixel
    for y in range(hauteur):
        for x in range(largeur):
            # Obtenir la couleur du pixel
            intensite_pixel = img.getpixel((x, y))
            bit_faible = intensite_pixel & 1

            # Ajouter le bit de poids faible à la clé binaire
            key_binary += str(bit_faible)
            if len(key_binary) == 64:
                return key_binary

# Exemple d'utilisation

image_modifiee = "rossignol2.bmp"
key = extract_key_from_bmp(image_modifiee)
print("Clé extraite de l'image BMP :", key)


