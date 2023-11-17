import os
import shutil

from PIL import Image, ImageChops

import json

# Chemin vers votre fichier JSON
file_path = 'json/data.json'

# Ouvrir le fichier JSON et charger les données
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)


def create_composite_image(output_path, background_path, overlay_path, image_path, element_path=None):
    # Charger le fond (calque 1), qui définira la taille de l'image finale
    background = Image.open(background_path).convert("RGBA")

    # Fonction pour centrer une image sur un fond transparent de la taille du fond
    def center_image(img, bg_size):
        new_img = Image.new("RGBA", bg_size, (0, 0, 0, 0))  # Créer un fond transparent
        position = ((bg_size[0] - img.size[0]) // 2, (bg_size[1] - img.size[1]) // 2)
        new_img.paste(img, position, img)
        return new_img

    # Fonction pour aligner une image en haut sur un fond transparent de la taille du fond
    def align_top_image(img, bg_size):
        new_img = Image.new("RGBA", bg_size, (0, 0, 0, 0))  # Créer un fond transparent
        position = ((bg_size[0] - img.size[0]) // 2, 0)  # Aligner en haut
        new_img.paste(img, position, img)
        return new_img

    # Charger et centrer les images
    overlay = center_image(Image.open(overlay_path).convert("RGBA"), background.size)
    image = align_top_image(Image.open(image_path).convert("RGBA"), background.size)

    # Appliquer le mode produit
    overlay_with_alpha = ImageChops.multiply(background, overlay)

    # Superposer le PNG sur le résultat du mode produit
    composite = Image.alpha_composite(overlay_with_alpha, image)

    if element_path:
        badge = center_image(Image.open(element_path).convert("RGBA"), background.size)
        # Superposer la pastille sur le résultat précédent
        composite = Image.alpha_composite(composite, badge)

    # Sauvegarder l'image résultante
    composite.save(output_path)


# Générer et sauvegarder les tableaux wiki pour les armes, calvities et items
for category in ['armes', 'calvs', 'items', 'familiers']:
    for x in data[category]:
        if "element" in x:
            create_composite_image(f'img/output/{category}/{x["name"]} skill.png', f'img/background.png',
                                   f'img/overlay/{x["rarity"]}.png', f'img/{category}/{x["short"]}.png',
                                   f'img/element/{x["element"]}.png')
        else:
            create_composite_image(f'img/output/{category}/{x["name"]} skill.png', f'img/background.png',
                                   f'img/overlay/{x["rarity"]}.png', f'img/{category}/{x["short"]}.png')
        print(x["name"])
