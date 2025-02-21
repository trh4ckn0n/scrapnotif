import requests
from bs4 import BeautifulSoup
import json

def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Récupérer les titres, les liens, et les descriptions (ajustez les sélecteurs selon votre besoin)
    articles = []
    
    # Exemple d'extraction des éléments sur une page de blog
    for article in soup.find_all('article'):  # En supposant que les articles sont dans des balises <article>
        title = article.find('h2', class_='post-title')  # Ajustez cette ligne selon la structure du site
        link = article.find('a', href=True)
        description = article.find('p')  # Une description pourrait être dans un <p> (ajustez le sélecteur)
        date = article.find('time')  # Si la date est dans une balise <time>

        if title:
            title_text = title.get_text(strip=True)
        else:
            title_text = "Titre non trouvé"
        
        link_url = link['href'] if link else "Lien non disponible"
        description_text = description.get_text(strip=True) if description else "Description non disponible"
        date_text = date.get_text(strip=True) if date else "Date non disponible"

        articles.append({
            'title': title_text,
            'link': link_url,
            'description': description_text,
            'date': date_text
        })
    
    return articles

def update_report(articles, filename='report.json'):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    
    # Mise à jour des informations
    data['latest_articles'] = articles
    
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def update_readme(articles, filename='README.md'):
    with open(filename, 'r') as f:
        content = f.read()

    # Créer un format propre pour afficher les articles dans le fichier README
    scraping_section = "\n## Scraping Results\n"
    if articles:
        scraping_section += "\nVoici les derniers articles extraits du site :\n"
        for article in articles:
            scraping_section += f"\n### {article['title']}\n"
            scraping_section += f"**Date**: {article['date']}\n"
            scraping_section += f"**Description**: {article['description']}\n"
            scraping_section += f"**Lien**: [Lire l'article]({article['link']})\n"
            scraping_section += "\n---\n"
    else:
        scraping_section += "Aucun article trouvé.\n"

    # Si la section "Scraping Results" existe déjà, on la remplace, sinon on l'ajoute
    if "## Scraping Results" in content:
        content = content.replace("## Scraping Results", scraping_section)
    else:
        content += scraping_section

    # Réécriture du fichier avec les articles mis à jour
    with open(filename, 'w') as f:
        f.write(content)

if __name__ == '__main__':
    url = 'https://www.alsetex.fr'  # Remplacer par le site réel
    articles = scrape_website(url)
    
    # Vérification que les articles sont bien extraits
    print("Scraped articles:", articles)

    update_report(articles)
    update_readme(articles)
