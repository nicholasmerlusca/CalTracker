import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
def get_nutrition(query: str, grams):
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    data = {"query": query,
            "api_key": API_KEY,
            "pageSize": 10}
    pagesize = 10

    response = requests.get(url, params=data)

    if response.status_code != 200:
        print("ERROR:", response.status_code, response.text)
        return None

    foods = response.json().get("foods", [])
    size = float(grams) / 100


    list_foods = []

    for food in foods:
        nutrients = {}

        for nutrient in food.get("foodNutrients", []):
            nutrient_id = nutrient.get("nutrientId")
            value = nutrient.get("value")

            nutrients[nutrient_id] = value

        # USDA nutrient IDs
        calories = nutrients.get(1008)  # Calories
        protein = nutrients.get(1003)  # Protein
        fat = nutrients.get(1004)  # Total fat
        carbs = nutrients.get(1005)  # Carbs

        list_foods.append({
            "food_name": food.get("description"),
            "nf_calories": calories * size if calories is not None else None,
            "nf_protein": protein * size if protein is not None else None,
            "nf_total_fat": fat * size if fat is not None else None,
            "nf_total_carbohydrate": carbs * size if carbs is not None else None,
            "nf_brand_name": food.get("brandName", "N/A")
        })

    return {"foods": list_foods}
