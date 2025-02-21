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

# Fonction pour mettre à jour le README.md
def update_readme(weather, temp, humidity, wind_speed):
    with open("README.md", "a", encoding="utf-8") as readme_file:
        readme_file.write(f"\n## Météo à {CITY} - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        readme_file.write(f"**Conditions:** {weather}\n")
        readme_file.write(f"**Température:** {temp}°C\n")
        readme_file.write(f"**Humidité:** {humidity}%\n")
        readme_file.write(f"**Vitesse du vent:** {wind_speed} m/s\n")

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
