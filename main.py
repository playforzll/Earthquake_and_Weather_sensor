import requests
from datetime import datetime
from random import choice, randint, shuffle


# Ask for user inputs: location and day

def SENSOR():
    Check = str(input("What do you want to check weather or earthquake\nweather/earthquake: "))

    if Check == "earthquake":
        location = input("Enter the location (type only city or country): ")
        print("")
        date = input("Enter the date (YYYY-MM-DD): ")

        # API URL to fetch earthquake data with a minimum magnitude of 1 (or 0)
        url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&minmagnitude=1&starttime={date}T00:00:00&endtime={date}T23:59:59"

        # Fetch the data from the API
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()

            # Filter earthquakes by location
            filtered_earthquakes = [
                earthquake for earthquake in data['features']
                if location.lower() in earthquake['properties']['place'].lower()
            ]

            # Check if any earthquakes match the location
            if filtered_earthquakes:
                print(f"\nEarthquakes in {location} on {date}:\n")
                for earthquake in filtered_earthquakes:
                    mag = earthquake['properties']['mag']
                    place = earthquake['properties']['place']
                    time = datetime.fromtimestamp(earthquake['properties']['time'] / 1000)
                    time = time.strftime("%Y-%m-%d %H:%M:%S")

                    if mag <= 3:
                        risk_emote = "(🟢 Low risk) "
                    elif 3 < mag < 6:
                        risk_emote = "(🟡 Medium risk) "
                    elif mag >= 6:
                        risk_emote = "(🔴 High risk) "
                    else:
                        risk_emote = ""

                    print(f"Location: {place} | Magnitude: {risk_emote}{mag} | Time: {time}")

            else:
                print(f"\nNo earthquakes found in {location} on {date}.")
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            SENSOR()

    elif Check == "weather":
        def get_lat(country1, city1):
            url1 = "https://nominatim.openstreetmap.org/search"
            params = {
                'q': f"{city1},{country1}",
                'format': 'json',
                'limit': 1
            }
            headers = {
                'User-Agent': "generate_name()"
            }
            response1 = requests.get(url1, params=params, headers=headers)
            data1 = response1.json()

            if data1:
                return data1[0]['lat']

        def get_lon(country2, city2):
            url2 = "https://nominatim.openstreetmap.org/search"
            params = {
                'q': f"{city2},{country2}",
                'format': 'json',
                'limit': 1
            }
            headers = {
                'User-Agent': "generate_name()"
            }
            response2 = requests.get(url2, params=params, headers=headers)
            data2 = response2.json()

            if data2:
                return data2[0]['lon']

        api_key = "aee6cad5c976956d9fb9bde4ce6d27ef"

        print("")
        country = str(input("Enter a country: "))
        city = str(input("Enter a city: "))
        print("")

        parameters = {
            "lat": get_lat(country, city),
            "lon": get_lon(country, city),
            "appid": api_key,
            "exclude": "current, minutely"
        }

        weather_response = requests.get("https://api.openweathermap.org/data/2.5/forecast", params=parameters)

        if weather_response.status_code == 200:
            weather_data = weather_response.json()
            for hour in weather_data["list"]:
                next_weather_condition_id_code = hour["weather"][0]["id"]
                if 200 <= next_weather_condition_id_code <= 299:
                    print("There's a thunderstorm expected. Stay safe from the thunderstorm!")
                elif 300 <= next_weather_condition_id_code <= 399:
                    print("Light rain is expected. Carry an umbrella!")
                elif 500 <= next_weather_condition_id_code <= 599:
                    print("Rain is expected. You must bring an umbrella!")
                elif 600 <= next_weather_condition_id_code <= 699:
                    print("Snow is expected. Dress warmly and stay safe!")
                elif 700 <= next_weather_condition_id_code <= 799:
                    print("It might be foggy or misty. Be careful when traveling!")
                elif next_weather_condition_id_code == 800:
                    print("Clear skies! It's a sunny day, enjoy!")
                elif 801 <= next_weather_condition_id_code <= 899:
                    print("Partly cloudy, perfect weather for outdoor activities.")
                break
        else:
            print("❗ Error: Unable to fetch data from the WEATHER API.\nCheck your connection or it is server issue")
            print(f"Response code: {weather_response.status_code}\n")
            SENSOR()

    else:
        print("I think you type something wrong. Please try again.\n")
        SENSOR()

    Try_again = str(input("\nWould you like to try again?\nYes/No: "))
    print("")
    Try_again = Try_again.upper()

    if Try_again == "YES":
        SENSOR()


SENSOR()
