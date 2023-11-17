import json

# Chemin vers votre fichier JSON
file_path = 'json/data.json'

# Ouvrir le fichier JSON et charger les données
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

print([{'name':fam["name"], 'element':fam['element'], 'desc': fam['desc']} for fam in data["familiers"]])

# Mapping des couleurs basé sur la rareté et l'élément
rarity_color_map = {
    0: "rgba(170,170,170,255)",
    1: "rgba(146,193,105,255)",
    2: "rgba(116,146,214,255)",
    3: "rgba(216,167,255,255)",
    4: "rgba(255,241,88,255)",
    5: "rgba(255,95,88,255)",
    6: "rgba(63,214,226,255)",
}

element_color_map = {
    "Banal": "rgba(170,170,170,255)",
    "Aqua": "rgba(116,146,214,255)",
    "Pyro": "rgba(255,95,88,255)",
    "Terra": "rgba(129,229,90,255)",
    "Électro": "rgba(255,241,88,255)",
    "Chaos": "rgba(216,167,255,255)",
    "Céleste": "rgba(63,214,226,255)",
}

# Mapping des en-têtes pour chaque type de tableau
headers_map = {
    'armes': ["Nom", "Rareté", "Élément", "Force", "PV", "Esquive", "Speed", "Effet(s) passif(s)", "Panoplie(s)",
              "Image"],
    'calvs': ["Nom", "Rareté", "Force", "PV", "Esquive", "Speed", "Effet(s) passif(s)", "Panoplie(s)", "Image"],
    'items': ["Nom", "Rareté", "Panoplie(s)", "Image"],
    'familiers': ["Nom", "Rareté", "Élément", "Force", "PV", "Esquive", "Speed", "Image"],
}

# Mapping des clés de tri pour chaque type de tableau avec support de tri multiple
sort_key_map = {
    'armes': [('rarity', True), ('name', True)],  # Trier d'abord par rareté (ascendant), puis par nom (ascendant)
    'calvs': [('rarity', True), ('name', True)],  # Trier par nom (ascendant)
    'items': [('panoplies', True), ('rarity', True)],  # Trier par effet (ascendant)
    'familiers': [('rarity', True), ('name', True)],  # Trier d'abord par vitesse (ascendant), puis par PV (ascendant)
}


# Fonction pour convertir les couleurs RGBA en hexadécimal
def rgba_to_hex(rgba_color):
    return '#{:02x}{:02x}{:02x}'.format(
        *tuple(int(x) for x in rgba_color.replace('rgba(', '').replace(')', '').split(',')[:3]))


# Fonction pour trier les données avec support de conditions multiples
def sort_data(data, sort_keys):
    if not sort_keys:
        return data

    def sort_by_keys(item):
        # Générer un tuple de valeurs de tri basées sur les clés de tri et l'ordre
        return tuple(item.get(key, 0) if asc else -item.get(key, 0) for key, asc in sort_keys)

    return sorted(data, key=sort_by_keys)


# Fonction pour générer le code wiki d'une entrée en utilisant les en-têtes
def generate_wiki_code(data, type):
    wiki_line = "|-\n"
    headers = headers_map[type]

    for header in headers:
        if header == "Nom":
            wiki_line += f"| [[{data.get('name', '')}]] "
        elif header == "Rareté":
            rarity = data.get('rarity', '')
            color = rgba_to_hex(rarity_color_map[rarity]) if rarity else ''
            wiki_line += f"|| style=\"background-color: {color}\" | {rarity} "
        elif header == "Élément":
            element = data.get('element', '')
            color = rgba_to_hex(element_color_map[element]) if element else ''
            wiki_line += f"|| style=\"background-color: {color}\" | {element} "
        elif header in ["Force", "PV", "Esquive", "Speed"]:
            if 'effect' in data:
                wiki_line += f"|| {data['effect'].get(header.lower(), '')} "
            elif 'stats' in data:
                wiki_line += f"|| {data['stats'].get(header.lower(), '')} "
        elif header == "Effet(s) passif(s)":
            passif_effects = data['effect'].get('passif', [])
            passif_text = ', '.join(
                f"[[{get_effect_name(effect[0])}]]: {effect[1]}" for effect in passif_effects) if passif_effects else ''
            wiki_line += f"|| {passif_text} "
        elif header == "Effet(s)":
            effects = data['effects']
            effects_text = ', '.join(
                f"[[{effect[0]}]]: {str(effect[1])}" for effect in data['effects']) if effects else ''
            wiki_line += f"|| {effects_text} "
        elif header == "Panoplie(s)":
            panoplies = data.get("panoplies", [])
            panoplies_text = ', '.join(f"[[{panoplie}]]" for panoplie in panoplies) if panoplies else ''
            wiki_line += f"|| {panoplies_text} "
        elif header == "Image":
            wiki_line += f"|| [[File:{data.get('short', 'placeholder')}.png|50px]]"

    wiki_line += "\n"
    return wiki_line

def get_effect_name(effect):
    return data['effectsv2'][effect]['name']


# Fonction pour créer le tableau wiki avec les en-têtes et les valeurs correspondantes
def create_wiki_table(data, type):
    # Récupérer les en-têtes pour le type donné
    headers = headers_map[type]

    # Créer l'en-tête du tableau wiki
    wiki_table = f"""==== Les {type.capitalize()} ====
{{| class="wikitable mw-collapsible mw-collapsed sortable" style="white-space:nowrap; width:100%;"
|+ style="text-align:left;" | [[{type.capitalize()} | Liste des {type} disponibles en jeu]]
|-\n! """ + ' !! '.join(headers) + "\n"

    # Ajouter les données dans le tableau
    for entry in data:
        wiki_table += generate_wiki_code(entry, type)

    # Fermer le tableau wiki
    wiki_table += "|}"
    return wiki_table


# Chemin vers votre fichier JSON
file_path = 'json/data.json'

# Ouvrir le fichier JSON et charger les données
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Générer et sauvegarder les tableaux wiki pour les armes, calvities et items
for category in ['armes', 'calvs', 'items', 'familiers']:
    # Récupérer les clés de tri pour la catégorie
    sort_keys = sort_key_map.get(category, [])
    # Tri des données avec les clés de tri
    table_data = sort_data(data[category], sort_keys)
    wiki_table = create_wiki_table(table_data, category)
    file_path = f'wiki_table_{category}.txt'
    with open(file_path, 'w', encoding='utf-8-sig') as file:
        file.write(wiki_table)

for color in element_color_map:
    print(color + ':' + rgba_to_hex(element_color_map[color]))

for color in rarity_color_map:
    print(str(color) + ':' + rgba_to_hex(rarity_color_map[color]))