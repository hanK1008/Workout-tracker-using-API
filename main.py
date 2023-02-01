import requests
import os
from datetime import datetime

APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"]
SHEETY_KEY = os.environ["Authorization"]

print(os.environ)


nutrition_url = "https://trackapi.nutritionix.com/v2/natural/exercise"
user_input = input("Which exercises you done today: ")

param = {
    "query": user_input,
    "gender": "male",
    "weight_kg": 73,
    "height_cm": 168,
    "age": 26
}

headers_param = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

response = requests.post(url=nutrition_url, headers=headers_param, json=param)
result = response.json()
response.raise_for_status()


# taking out all the data from the required data from above exercise result
# Sheety API to populate the Google sheet
sheety_endpoint = "https://api.sheety.co/663a8a417d8a4a09c44d6b2e74dd5c74/myWorkoutsPython/workouts"
result_list = result["exercises"]
for exercise in result_list:
    exercise_duration = exercise["duration_min"]
    calories = exercise["nf_calories"]
    exercise_type = exercise["name"].title()
    current_date = datetime.now()
    today_date = current_date.strftime("%d/%m/%Y")
    current_time = current_date.strftime("%X")

    exercise_params = {
        "workout": {
            "date": today_date,
            "time": current_time,
            "exercise": exercise_type,
            "duration": exercise_duration,
            "calories": calories
        }
    }
    exercise_header = {
        "Authorization": SHEETY_KEY,
        "Content-Type": "application/json"
    }
    response = requests.post(url=sheety_endpoint, json=exercise_params, headers = exercise_header)
    response.raise_for_status()


print("Cheers: Your data added to your google sheet.....")







