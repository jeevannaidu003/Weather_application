import requests
import tkinter as tk
import tkintermapview

api_key = "61b56602e3ef0e174c2a48d0a1ae304c"

weather_url = "https://api.openweathermap.org/data/2.5/weather"
ip_url = "http://ip-api.com/json/"

def get_location():
    try:
        data = requests.get(ip_url).json()
        return data.get("lat"), data.get("lon"), data.get("city")
    except:
        return None, None, None

def get_emoji(condition):
    condition = condition.lower()

    if "clear" in condition:
        return "☀️"
    elif "cloud" in condition:
        return "☁️"
    elif "rain" in condition:
        return "🌧️"
    elif "thunder" in condition:
        return "⛈️"
    elif "snow" in condition:
        return "❄️"
    elif "mist" in condition or "fog" in condition:
        return "🌫️"
    else:
        return "🌍"

def fetch_weather(city=None, lat=None, lon=None):
    params = {"appid": api_key, "units": "metric"}

    if city:
        params["q"] = city
    else:
        params["lat"] = lat
        params["lon"] = lon

    try:
        response = requests.get(weather_url, params=params)

        data = response.json()

        if data.get("cod") != 200:
            result_label.config(text=f"Error: {data.get('message')}", fg="red")
            return

        city_name = data["name"]
        temp = data["main"]["temp"]
        condition = data["weather"][0]["description"].title()

        emoji = get_emoji(condition)

        result_label.config(
            text=f"{emoji}\n{city_name}\n{temp}°C\n{condition}",
            fg="white"
        )

        map_widget.set_position(
            lat if lat else data["coord"]["lat"],
            lon if lon else data["coord"]["lon"]
        )
        map_widget.set_zoom(10)

    except Exception as e:
        print("ERROR:", e)
        result_label.config(text="Network error", fg="red")

def search():
    city = entry.get().strip()
    if city:
        fetch_weather(city=city)

root = tk.Tk()
root.title("Weather App")
root.geometry("700x700")

canvas = tk.Canvas(root, width=700, height=700)
canvas.pack(fill="both", expand=True)

frame = tk.Frame(root, bg="#1e1e2f")
frame.place(relwidth=0.9, relheight=0.9, relx=0.05, rely=0.05)

title = tk.Label(frame, text="Weather App", bg="#1e1e2f", fg="white", font=("Arial", 20, "bold"))
title.pack(pady=10)

entry = tk.Entry(frame, font=("Arial", 14))
entry.pack(pady=10)

search_btn = tk.Button(frame, text="Search", command=search, bg="#4caf50", fg="white")
search_btn.pack(pady=10)

result_label = tk.Label(frame, text="", bg="#1e1e2f", fg="white", font=("Arial", 20, "bold"))
result_label.pack(pady=10)

map_widget = tkintermapview.TkinterMapView(frame, width=500, height=300)
map_widget.pack(pady=10)

lat, lon, city = get_location()
if lat and lon:
    fetch_weather(lat=lat, lon=lon)

root.mainloop()