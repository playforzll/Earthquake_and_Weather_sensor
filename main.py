import requests
from datetime import datetime


# Ask for user inputs: location and day
def SENSOR():
    Check = str(input("What do you want to check weather or earthquake\nweather/earthquake: "))

    if Check == "earthquake":
        location = input("Enter the location (type only city or country): ")
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
        api_key = "aee6cad5c976956d9fb9bde4ce6d27ef"

        parameters = {
            "lat": 21.916222,
            "lon": 95.955971,
            "appid": api_key,
            "exclude": "current, minutely"
        }

        weather_response = requests.get("https://api.openweathermap.org/data/2.5/forecast", params=parameters)

        if weather_response.status_code == 200:
            weather_data = weather_response.json()
            for hour in weather_data["list"]:
                next_weather_condition_id_code = hour["weather"][0]["id"]
                if int(next_weather_condition_id_code) < 700:
                    print("Today is going to rain\n\nYou must bring an umbrella!")
                elif int(next_weather_condition_id_code) > 700:
                    print(
                        "Today is sunny. You must bring an umbrella to get some shade, sunglasses and also sunscreen.")
                break
        else:
            print("❗ Error: Unable to fetch data from the WEATHER API.\nCheck your connection or it is server issue")
            print(f"Response code: {weather_response.status_code}\n")
            SENSOR()

    else:
        print("I think you type something wrong. Please try again.\n")
        SENSOR()

    Try_again = str(input("\nWould you like to try again?\nYes/No: \n"))
    Try_again = Try_again.upper()

    if Try_again == "YES":
        SENSOR()


SENSOR()
