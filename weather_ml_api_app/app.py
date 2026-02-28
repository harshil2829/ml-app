
from flask import Flask, render_template, request
import requests
import numpy as np
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

API_KEY = "YOUR_OPENWEATHER_API_KEY"

def fetch_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    temps = []
    for item in data["list"][:10]:
        temps.append(item["main"]["temp"])
    
    return temps

def train_model(temps):
    X = np.array(range(len(temps))).reshape(-1, 1)
    y = np.array(temps)
    
    model = LinearRegression()
    model.fit(X, y)
    
    next_day = np.array([[len(temps)]])
    prediction = model.predict(next_day)[0]
    
    return round(prediction, 2)

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    error = None
    
    if request.method == "POST":
        city = request.form["city"]
        
        try:
            temps = fetch_weather(city)
            prediction = train_model(temps)
        except Exception:
            error = "Error fetching data. Check city name or API key."
    
    return render_template("index.html", prediction=prediction, error=error)

if __name__ == "__main__":
    app.run(debug=True)
