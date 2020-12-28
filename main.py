import requests
import os
from datetime import datetime
import google

NUTRITIONIX_API_URL = "https://trackapi.nutritionix.com/v2/natural/exercise"
NUTRITIONIX_APP_ID = os.environ['NUTRITIONIX_APP_ID']
NUTRITIONIX_APP_KEY = os.environ['NUTRITIONIX_APP_KEY']
SHEETY_API_URL = "https://v2-api.sheety.co/2a910e6bf759cd9eaf52575d521dadbd/myWorkoutsPythonApi/workouts"
SHEETS_CLIENT_ID = os.environ['GOOGLE_SHEETS_API_CLIENT_ID']
SHEETS_CLIENT_SECRET = os.environ['GOOGLE_SHEETS_API_CLIENT_SECRET']
SHEETY_AUTH = os.environ['SHEETY_AUTH']
now_date = datetime.now().strftime("%m/%d/%Y")
now_time = datetime.now().strftime("%H:%M:%S")

ntx_headers = {
    "x-app-id": NUTRITIONIX_APP_ID,
    "x-app-key": NUTRITIONIX_APP_KEY
}

exercise_nl_text = "Run 3 miles" #input("What exercise did you do today? ")

ntx_params = {
    "query": exercise_nl_text
}

exercise_data = requests.post(url=NUTRITIONIX_API_URL, json=ntx_params, headers=ntx_headers).json()['exercises']
print(exercise_data)

sheety_headers = {
    "Authorization": SHEETY_AUTH
}

for row in exercise_data:
    exercise = row['user_input']
    duration = row['duration_min']
    calories = row['nf_calories']

    row_params = {
        "workout": {
            "date": now_date,
            "time": now_time,
            "exercise": exercise.title(),
            "duration": int(duration),
            "calories": int(calories)
        }
    }

    print(row_params)
    add_row_response = requests.post(url=SHEETY_API_URL, json=row_params, headers=sheety_headers).json()
    print(add_row_response)