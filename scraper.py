import requests
from bs4 import BeautifulSoup
import os
import json
import time
import random

# Fonction pour envoyer une requête HTTP et récupérer le contenu HTML de la page
def fetch_page(url, headers=None, params=None):
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération de la page : {e}")
        return None

# Fonction pour parser le contenu HTML avec BeautifulSoup
def parse_html(html_content):
    return BeautifulSoup(html_content, 'html.parser')

# Fonction pour extraire les liens d'images
def extract_images(soup):
    images = []
    for img_tag in soup.find_all('img'):
        img_url = img_tag.get('src')
        if img_url:
            images.append(img_url)
    return images

# Fonction pour extraire les liens des fichiers CSS
def extract_css(soup):
    css_links = []
    for link_tag in soup.find_all('link', rel='stylesheet'):
        css_url = link_tag.get('href')
        if css_url:
            css_links.append(css_url)
    return css_links

# Fonction pour extraire les scripts JS
def extract_scripts(soup):
    scripts = []
    for script_tag in soup.find_all('script', src=True):
        script_url = script_tag.get('src')
        if script_url:
            scripts.append(script_url)
    return scripts

# Fonction pour sauvegarder les résultats dans un fichier JSON
def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Fonction pour faire une pause aléatoire entre les requêtes (utile pour éviter de surcharger le serveur)
def random_pause(min_seconds=1, max_seconds=3):
    time.sleep(random.uniform(min_seconds, max_seconds))

# Fonction principale de scraping qui intègre toutes les étapes
def scrape_page(url, headers=None, params=None, output_dir='output'):
    # Créer un répertoire de sortie si nécessaire
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Récupérer et parser la page
    html_content = fetch_page(url, headers, params)
    if not html_content:
        print("Échec du scraping.")
        return

    soup = parse_html(html_content)

    # Extraire les données souhaitées
    images = extract_images(soup)
    css_links = extract_css(soup)
    scripts = extract_scripts(soup)

    # Enregistrer les résultats dans des fichiers
    save_to_json(images, os.path.join(output_dir, 'images.json'))
    save_to_json(css_links, os.path.join(output_dir, 'css_links.json'))
    save_to_json(scripts, os.path.join(output_dir, 'scripts.json'))

    print(f"Scraping terminé. Résultats sauvegardés dans '{output_dir}'.")

# Exemple d'utilisation
if __name__ == "__main__":
    url_to_scrape = 'https://www.alsetex.fr/'  # Remplacer par l'URL de la page cible
    scrape_page(url_to_scrape)
