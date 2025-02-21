import requests
from bs4 import BeautifulSoup
import json

def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Exemple: extraire les titres des articles d'un blog
    titles = [title.get_text() for title in soup.find_all('h2', class_='post-title')]
    
    return titles

def update_report(titles, filename='report.json'):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    
    # Mise à jour des informations
    data['latest_titles'] = titles
    
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == '__main__':
    url = 'https://www.alsetex.fr'  # Remplacer par le site réel
    titles = scrape_website(url)
    update_report(titles)
