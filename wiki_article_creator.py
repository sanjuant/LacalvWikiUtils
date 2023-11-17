from PIL import Image, ImageChops


def create_composite_image(background_path, overlay_path, image_path, badge_path):
    # Charger le fond (calque 1), qui définira la taille de l'image finale
    background = Image.open(background_path).convert("RGBA")

    # Fonction pour centrer une image sur un fond transparent de la taille du fond
    def center_image(img, bg_size):
        new_img = Image.new("RGBA", bg_size, (0, 0, 0, 0))  # Créer un fond transparent
        position = ((bg_size[0] - img.size[0]) // 2, (bg_size[1] - img.size[1]) // 2)
        new_img.paste(img, position, img)
        return new_img

    # Charger et centrer les images
    overlay = center_image(Image.open(overlay_path).convert("RGBA"), background.size)
    image = center_image(Image.open(image_path).convert("RGBA"), background.size)
    badge = center_image(Image.open(badge_path).convert("RGBA"), background.size)

    # Appliquer le mode produit
    overlay_with_alpha = ImageChops.multiply(background, overlay)

    composite = Image.alpha_composite(overlay_with_alpha, badge)
    # Superposer le PNG sur le résultat du mode produit
    composite_with_badge = Image.alpha_composite(composite, image)

    # Superposer la pastille sur le résultat précédent

    # Sauvegarder l'image résultante
    composite_with_badge.save("composite_image.png")

    return composite_with_badge


# Exemple d'utilisation de la fonction avec des chemins fictifs et une position fictive pour la pastille
# Vous devrez remplacer 'background.png', 'overlay.png', etc. par les chemins de vos propres fichiers
# Et (50, 50) par les coordonnées x, y où vous voulez placer la pastille

# Veuillez noter que les fichiers ne sont pas présents dans cet environnement,
# ce code est uniquement à titre d'exemple et ne sera pas exécuté ici.
create_composite_image('img/background.png', 'img/overlay/4.png', 'img/familier/potofeu.png', 'img/element/pyro.png')
