import requests
from datetime import datetime
import pytz

# Clé API OpenWeatherMap (à remplacer si nécessaire)
API_KEY = "c7381d724afbdc1e5e150a2482400341"

# Liste des villes
CITIES = ["Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Nantes", "Strasbourg", "Montpellier", "Bordeaux", "Lille", "Gaza", "Kiev"]

# Dictionnaire pour les emojis en fonction des conditions météo en français
weather_emojis = {
    "ciel dégagé": "🌞",  # Ciel dégagé
    "quelques nuages": "🌤️",  # Quelques nuages
    "nuages épars": "🌥️",  # Nuages épars
    "nuages fragmentés": "☁️",  # Nuages fragmentés
    "pluie modérée": "🌧️",  # Pluie modérée
    "pluie": "🌧️",  # Pluie
    "orage": "🌩️",  # Orage
    "neige": "❄️",  # Neige
    "brume": "🌫️",  # Brume
    "brouillard": "🌫️",  # Brouillard
    "poussière": "🌪️",  # Poussière
    "sable": "🌪️",  # Sable
    "cendres volcaniques": "🌋",  # Cendres volcaniques
    "rafales": "🌬️",  # Rafales
    "tornade": "🌪️"  # Tornade
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

        # Réécriture du fichier README.md
        with open("README.md", "w", encoding="utf-8") as readme_file:
            readme_file.write(new_weather_info)

        print("✅ Météo mise à jour avec succès.")

    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour du README.md : {e}")

# Fonction principale
def main():
    weather_data = [get_weather_data(city) for city in CITIES]
    update_readme(weather_data)

if __name__ == "__main__":
    main()
