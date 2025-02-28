import requests
from datetime import datetime
import pytz
import matplotlib.pyplot as plt
import numpy as np
# Clé API OpenWeatherMap (à remplacer si nécessaire)
API_KEY = "c7381d724afbdc1e5e150a2482400341"

# Liste des villes
CITIES = ["Strasbourg", "Mulhouse", "Montbéliard", "Besançon", "Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Nantes", "Strasbourg", "Montpellier", "Bordeaux", "Lille", "Gaza", "Kiev"]

# Dictionnaire pour les emojis en fonction des conditions météo en français
weather_emojis = {
    "ciel dégagé": "☀️",  # Ciel dégagé
    "quelques nuages": "🌤️",  # Quelques nuages
    "nuages épars": "🌥️",  # Nuages épars
    "nuages fragmentés": "🌥️",  # Nuages fragmentés
    "pluie modérée": "🌧️",  # Pluie modérée
    "pluie": "🌧️",  # Pluie
    "averse de pluie": "🌧️",  # Averse de pluie
    "orage": "⚡",  # Orage
    "neige": "❄️",  # Neige
    "légère pluie": "🌧️",
    "neige légère": "🌨️",  # Neige légère
    "brume": "🌫️",  # Brume
    "brouillard": "🌫️",  # Brouillard
    "poussière": "🌪️",  # Poussière
    "sable": "🌪️",  # Sable
    "cendres volcaniques": "🌋",  # Cendres volcaniques
    "rafales": "🌬️",  # Rafales
    "vent fort": "🌬️",  # Vent fort
    "tornade": "🌪️",  # Tornade
    "pluie verglaçante": "🌨️",  # Pluie verglaçante
    "givre": "❄️",  # Givre
    "tempête de neige": "🌨️",  # Tempête de neige
    "froid extrême": "🥶",  # Froid extrême
    "chaleur extrême": "🥵",  # Chaleur extrême
    "humidité élevée": "💧",  # Humidité élevée
    "éclaircies": "🌤️",  # Éclaircies
}

# Fonction pour obtenir les données météo d'une ville
def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=fr"  # Langue française
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        weather_condition = data["weather"][0]["description"]
        emoji = weather_emojis.get(weather_condition, "🌥️")  # Par défaut, utilisez un emoji de nuages
        return {
            "city": city,
            "weather": weather_condition,
            "emoji": emoji,
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
    else:
        print(f"❌ Erreur avec {city} - Code {response.status_code}")
        return {"city": city, "weather": None}

# Fonction pour créer un graphique d'humidité


def create_humidity_chart(weather_data):
    # Filtrer les données valides
    cities = [data["city"] for data in weather_data if data["humidity"] is not None]
    humidity_values = [data["humidity"] for data in weather_data if data["humidity"] is not None]

    # Création de la figure
    plt.figure(figsize=(12, 6))
    
    # Dégradé de couleurs pour les barres
    bar_colors = plt.cm.coolwarm(np.linspace(0, 1, len(humidity_values)))  # Utilisation d'un dégradé de couleurs
    
    bars = plt.bar(cities, humidity_values, color=bar_colors, edgecolor="black", linewidth=1.5)

    # Ajouter des titres et des labels avec des polices stylées
    plt.title("Taux d'humidité des villes", fontsize=16, fontweight='bold', color="white", backgroundcolor='purple')
    plt.xlabel("Villes", fontsize=14, fontweight='bold', color="white")
    plt.ylabel("Humidité (%)", fontsize=14, fontweight='bold', color="white")
    
    # Ajouter des annotations au-dessus des barres
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 2, f'{yval}%', ha='center', fontsize=10, color="black")

    # Améliorer la présentation des étiquettes de l'axe des X
    plt.xticks(rotation=45, ha="right", fontsize=12, color="white")

    # Ajouter une grille avec une couleur discrète
    plt.grid(True, linestyle="--", color="white", alpha=0.3)
    
    # Personnaliser l'arrière-plan de la figure
    plt.gcf().set_facecolor('#2a2a2a')  # Fond sombre

    # Ajuster la disposition pour éviter les chevauchements
    plt.tight_layout()

    # Sauvegarder le graphique
    plt.savefig("humidity_chart.png", dpi=300)  # Sauvegarder avec une résolution haute qualité
    plt.close()

# Fonction pour mettre à jour le README.md
def update_readme(weather_data):
    try:
        # Contenu météo
        new_weather_info = "## Météo des grandes villes + Gaza et Kiev 🌍\n"
        paris_tz = pytz.timezone('Europe/Paris')  # Définir le fuseau horaire de Paris
        current_time = datetime.now(paris_tz)
        new_weather_info += f"🕒 Mise à jour : {current_time.strftime('%d/%m/%Y %H:%M:%S')}\n\n"

        for data in weather_data:
            city = data["city"]
            if data["weather"]:
                new_weather_info += f"### 🌍 {city} {data['emoji']}\n"
                new_weather_info += f"**Conditions :** {data['weather']}\n"
                new_weather_info += f"**Température :** {data['temp']}°C\n"
                new_weather_info += f"**Humidité :** {data['humidity']}%\n"
                new_weather_info += f"**Vent :** {data['wind_speed']} m/s\n\n"
            else:
                new_weather_info += f"### 🌍 {city}\n❌ Erreur de récupération des données météo\n\n"

        # Ajout du graphique d'humidité
        new_weather_info += f"<p align='center'><img src='https://raw.githubusercontent.com/khoa083/khoa/main/Khoa_ne/img/Rainbow.gif' width='100%' style='border-radius: 5px; border: 3px solid #39FF14; box-shadow: 0 0 10px #39FF14, 0 0 20px #39FF14;' /></p><br>"

        # Ajouter ensuite les informations suivantes
        new_weather_info += "### 🌡️ Graphique d'humidité des villes\n"
        new_weather_info += "![Graphique d'humidité](humidity_chart.png)\n"        
        new_weather_info += f"<p align='center'><img src='https://raw.githubusercontent.com/khoa083/khoa/main/Khoa_ne/img/Rainbow.gif' width='100%' style='border-radius: 5px; border: 3px solid #39FF14; box-shadow: 0 0 10px #39FF14, 0 0 20px #39FF14;' /></p>"

        # Réécriture du fichier README.md
        with open("README.md", "w", encoding="utf-8") as readme_file:
            readme_file.write(new_weather_info)

        print("✅ Météo mise à jour avec succès.")

    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour du README.md : {e}")

# Fonction principale
def main():
    weather_data = [get_weather_data(city) for city in CITIES]
    create_humidity_chart(weather_data)  # Créer le graphique d'humidité
    update_readme(weather_data)

if __name__ == "__main__":
    main()
