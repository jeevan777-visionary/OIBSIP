
import tkinter as tk
from tkinter import messagebox
import requests

# Replace with your actual API key from OpenWeatherMap
API_KEY = "1f01b1cdb2ac6cd31e08f7904580340c"

def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            messagebox.showerror("Error", data.get("message", "Unknown error occurred."))
            return

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        condition = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]

        result = f"Temperature: {temp}°C\nHumidity: {humidity}%\nCondition: {condition}\nWind Speed: {wind_speed} m/s"
        weather_result.config(text=result)

    except Exception as e:
        messagebox.showerror("Error", f"Could not retrieve weather data.\n{e}")

# GUI Setup
root = tk.Tk()
root.title("Weather App")
root.geometry("400x300")

tk.Label(root, text="Enter City:", font=("Arial", 12)).pack(pady=10)
city_entry = tk.Entry(root, font=("Arial", 12))
city_entry.pack(pady=5)

tk.Button(root, text="Get Weather", command=get_weather, font=("Arial", 12)).pack(pady=10)

weather_result = tk.Label(root, text="", font=("Arial", 12), justify="left")
weather_result.pack(pady=20)

root.mainloop()
