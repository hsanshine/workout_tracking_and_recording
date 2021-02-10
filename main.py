import os
import requests
from datetime import datetime

GENDER = 'male'
WEIGHT = 70
HEIGHT = 183
AGE = 22
SHEETY_PROJECT = os.environ.get('SHEETY_PROJECT')
SHEETY_SHEET = os.environ.get('SHEETY_SHEET')
SHEETY_USERNAME = os.environ.get('SHEETY_USERNAME')

NUTRITION_API_KEY = os.environ.get('NUTRITION_API_KEY')
NUTRITION_API_ID = os.environ.get('NUTRITION_API_ID')
nutrition_api_endpoint = 'https://trackapi.nutritionix.com/v2/natural/exercise'

sheety_api_endpoint = 'https://api.sheety.co'
sheety_add_row_endpoint = f'{sheety_api_endpoint}/{SHEETY_USERNAME}/{SHEETY_PROJECT}/{SHEETY_SHEET}'

headers = {
    "x-app-id": NUTRITION_API_ID,
    "x-app-key": NUTRITION_API_KEY,
}

workouts = input('enter the exercises that you did: ')

exercise_parameters = {
    "query": workouts,
    "gender": GENDER,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE
}

response = requests.post(url=nutrition_api_endpoint, json=exercise_parameters, headers=headers)
data = response.json()
rows = [(dic['name'], dic['duration_min'], dic['nf_calories']) for dic in data['exercises']]
current_time = datetime.now().time().strftime('%H:%M:%S')
current_date = datetime.now().date().strftime('%d/%m/%Y')

for row in rows:
    entry = {
        "workout": {
            'date': current_date,
            'time': current_time,
            "exercise": row[0].title(),
            "duration": row[1],
            "calories": row[2],
        }
    }
    response = requests.post(url=sheety_add_row_endpoint, json=entry, auth=(os.environ.get('user_name'),
                                                                            os.environ.get('password')))
    
