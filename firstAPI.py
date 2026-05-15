import sys
import requests  #Imports the requests to give API
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout)    #Basic app development widgets

from PyQt5.QtCore import Qt


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)                           #Assigning variables to their location on PyQt5.QtWidgets
        self.weather_button = QPushButton("Get Weather", self)
        self.temp_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")  #Names the pop up window "Weather App"

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.weather_button)     #Adds buttons and creates a neat layout
        vbox.addWidget(self.temp_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)           #Centers the buttons and words
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.weather_button.setObjectName("weather_button")         #Assigns an easy name for the variables to be called from
        self.temp_label.setObjectName("temp_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
                           
            QLabel, QPushButton
            {
                font-family: Times New Roman;
            }

            QLabel#city_label
            {
                font-size: 40px;
            }
                           
            QLineEdit#city_input
            {
                font-size: 20px;
            }
                           
            QPushButton#weather_button
            {
                font-size: 30px
            }
                           
            QLabel#temp_label
            {
                font-size: 40px
            }
                           
            QLabel#description_label
            {
                font-size: 30px
            }
        """)

        self.weather_button.clicked.connect(self.get_weather)   #Makes the button function

    def get_weather(self):
        api_key = "28f3739da8ad4203d10cb3b899f39626"        #When the button is clicked, it will retrieve data from an online weather API
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()    #Checks for any other Error number besides "200"
            data = response.json()   #Converts data from API into a Python dictionary 

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            if response.status_code == 400:
                self.display_error("Error: Server cannot process your request (Check your input)")
            elif response.status_code == 401:
                self.display_error("Unauthorized: Invalid API key")
            elif response.status_code == 403:
                self.display_error("Forbidden: Access Denied")
            elif response.status_code == 404:
                self.display_error("Error: City not found")
            elif response.status_code == 500:
                self.display_error("Internal Server Error: Please try again later")
            elif response.status_code == 502:
                self.display_error("Bad Gateway: Invalid server response")
            elif response.status_code == 503:
                self.display_error("Error: Server is down")
            elif response.status_code == 504:
                self.display_error("Gateway Timeout: No Response from Server")
            elif response.status_code == _:
                self.display_error(f"HTTP Error: {http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error: Check your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Time Out Error: The request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Redirection Error: Check URL")
        except requests.exceptions.RequestException as request_error:
            self.display_error(f"Request Error: {request_error}")


    def display_error(self, message):
        self.temp_label.setStyleSheet("font-size: 20px;")
        self.temp_label.setText(message)
        self.description_label.clear()      #Clears previously printed data when there is an Error

    def display_weather(self, data):
        self.temp_label.setStyleSheet("font-size: 40px;")
        temp_kelvin = data["main"]["temp"]
        temp_farenheight = (temp_kelvin * 9/5) - 459.67
        self.temp_label.setText(f"{temp_farenheight:.1f} F")
        
        weather_description = data["weather"][0]["description"]
        self.description_label.setText(weather_description)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()     #Generates the pop up window
    sys.exit(app.exec_())  #Keeps the pop up window untill the user closes it