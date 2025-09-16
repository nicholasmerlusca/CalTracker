import CalTrack_api

def main():
    meal = input("What did you eat?\n")
    nutrition_data = CalTrack_api.get_nutrition(meal)

    if nutrition_data:
        print("\n nutrition info:")
        for food in nutrition_data["foods"]:
            print(f"- {food['food_name'].title()}: "
                  f"{food['nf_calories']} kcal | "
                  f"P: {food['nf_protein']}g | "
                  f"C: {food['nf_total_carbohydrate']}g | "
                  f"F: {food['nf_total_fat']}g")

if __name__ == '__main__':
    main()
