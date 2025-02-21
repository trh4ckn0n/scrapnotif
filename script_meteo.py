import requests
from datetime import datetime

# Votre clé API OpenWeatherMap
API_KEY = "c7381d724afbdc1e5e150a2482400341"
CITY = "Strasbourg"  # Ville de l'Est de la France, vous pouvez changer pour une autre

# Fonction pour obtenir les données météo
def get_weather_data():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY},FR&appid={API_KEY}&units=metric&lang=fr"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        return weather, temp, humidity, wind_speed
    else:
        return None

# Fonction pour mettre à jour le README.md (remplacer l'ancienne météo)
def update_readme(weather, temp, humidity, wind_speed):
    try:
        # Lire le contenu du README.md
        with open("README.md", "r", encoding="utf-8") as readme_file:
            content = readme_file.read()

        # Trouver et remplacer la section de la météo précédente
        updated_content = content
        start_index = updated_content.find("## Météo à {}".format(CITY))
        if start_index != -1:
            end_index = updated_content.find("##", start_index + 1)  # Chercher le prochain en-tête de section
            if end_index == -1:
                end_index = len(updated_content)
            updated_content = updated_content[:start_index] + updated_content[end_index:]

        # Ajouter la nouvelle météo
        new_weather_info = f"## Météo à {CITY} - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
        new_weather_info += f"**Conditions:** {weather}\n"
        new_weather_info += f"**Température:** {temp}°C\n"
        new_weather_info += f"**Humidité:** {humidity}%\n"
        new_weather_info += f"**Vitesse du vent:** {wind_speed} m/s\n"

        updated_content += new_weather_info

        # Réécrire le README.md avec la nouvelle météo
        with open("README.md", "w", encoding="utf-8") as readme_file:
            readme_file.write(updated_content)

    except Exception as e:
        print(f"Erreur lors de la mise à jour du README.md : {e}")

# Fonction principale
def main():
    weather, temp, humidity, wind_speed = get_weather_data()
    if weather:
        update_readme(weather, temp, humidity, wind_speed)
        print("Météo mise à jour dans README.md avec succès.")
    else:
        print("Erreur lors de la récupération des données météo.")

if __name__ == "__main__":
    main()
