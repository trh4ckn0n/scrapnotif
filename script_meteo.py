import requests
from datetime import datetime

# Clé API OpenWeatherMap
API_KEY = "c7381d724afbdc1e150a2482400341"

# Liste des villes importantes + Gaza et Kiev
CITIES = ["Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Nantes", "Strasbourg", "Montpellier", "Bordeaux", "Lille", "Gaza", "Kiev"]

# Fonction pour obtenir les données météo d'une ville
def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=fr"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        return city, weather, temp, humidity, wind_speed
    else:
        return city, None, None, None, None

# Fonction pour mettre à jour le README.md
def update_readme(weather_data):
    try:
        # Lire le contenu existant du README.md
        with open("README.md", "r", encoding="utf-8") as readme_file:
            content = readme_file.read()

        # Supprimer les anciennes données météo
        start_index = content.find("## Météo des grandes villes")
        if start_index != -1:
            end_index = content.find("##", start_index + 1)
            if end_index == -1:
                end_index = len(content)
            content = content[:start_index] + content[end_index:]

        # Ajouter les nouvelles données météo
        new_weather_info = "## Météo des grandes villes + Gaza et Kiev 🌍\n"
        new_weather_info += f"🕒 Mise à jour : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"

        for city, weather, temp, humidity, wind_speed in weather_data:
            if weather:
                new_weather_info += f"### 🌍 {city}\n"
                new_weather_info += f"**Conditions :** {weather}\n"
                new_weather_info += f"**Température :** {temp}°C\n"
                new_weather_info += f"**Humidité :** {humidity}%\n"
                new_weather_info += f"**Vent :** {wind_speed} m/s\n\n"
            else:
                new_weather_info += f"### 🌍 {city}\n❌ Erreur de récupération des données météo\n\n"

        # Écrire les nouvelles infos dans le README.md
        with open("README.md", "w", encoding="utf-8") as readme_file:
            readme_file.write(content + new_weather_info)

        print("Météo mise à jour dans README.md avec succès.")

    except Exception as e:
        print(f"Erreur lors de la mise à jour du README.md : {e}")

# Fonction principale
def main():
    weather_data = [get_weather_data(city) for city in CITIES]
    update_readme(weather_data)

if __name__ == "__main__":
    main()
