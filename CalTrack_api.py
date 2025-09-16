import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
APP_ID = os.getenv("APP_ID")

def get_nutrition(query: str):
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {"x-app-id": APP_ID, "x-app-key": API_KEY, "content-type": "application/json"}
    data = {"query": query}

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print("ERROR:", response.status_code, response.text)
        return None
