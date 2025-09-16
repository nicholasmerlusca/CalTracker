import CalTrack_api

diet = {"calories": 0.0, "protein": 0.0, "fat": 0.0, "carbs": 0.0 }
def main():
    running = True
    while running:

        meal = input("What did you eat?\n")
        # get nutrition data from API
        nutrition_data = CalTrack_api.get_nutrition(meal)


        if nutrition_data:
            print("\n nutrition info:")
            for food in nutrition_data["foods"]:
                print(f"- {food['food_name'].title()}: "
                      f"{food['nf_calories']} kcal | "
                      f"P: {food['nf_protein']}g | "
                      f"C: {food['nf_total_carbohydrate']}g | "
                      f"F: {food['nf_total_fat']}g")


            print(f"would you like to log this? Y/N")
            if input().lower() == 'y':
                for food in nutrition_data["foods"]:
                    diet["calories"] += food["nf_calories"]
                    diet["protein"] += food["nf_protein"]
                    diet["fat"] += food["nf_total_fat"]
                    diet["carbs"] += food["nf_total_carbohydrate"]
            print("Current stats for the day: \n")
            print_diet()
        if input("would you like to add something else? Y/N\n").lower() == 'n':
            running = False
    print("Thank you for using CalTrack!")
def print_diet():
    for macro in diet:
        print(f'{macro}:  {diet[macro]}')
if __name__ == '__main__':
    main()
