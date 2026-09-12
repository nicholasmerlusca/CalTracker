import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
def get_nutrition(query: str, grams):
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    data = {"query": query,
            "api_key": API_KEY}

    response = requests.get(url, params=data)
    if response.status_code == 200:
        list_foods = []
        size = float(grams)/100
        resp = response.json().get("foods", [])[0:10]
        for food in resp:
            list_foods.append({
                "food_name": food.get("description"),
                "nf_calories": food.get("foodNutrients", [])[3].get("value")*size if len(food.get("foodNutrients", [])) > 3 else None,
                "nf_protein": food.get("foodNutrients", [])[0].get("value")*size if len(food.get("foodNutrients", [])) > 0 else None,
                "nf_total_fat": food.get("foodNutrients", [])[1].get("value")*size if len(food.get("foodNutrients", [])) > 1 else None,
                "nf_total_carbohydrate": food.get("foodNutrients", [])[2].get("value")*size if len(food.get("foodNutrients", [])) > 2 else None,
                "nf_brand_name": food.get("brandName", "N/A")
            })
        return {"foods": list_foods}



    else:
        print("ERROR:", response.status_code, response.text)
        return None
if __name__ == '__main__':
    import json
    result = get_nutrition("egg")
    print(json.dumps(result, indent=2))
