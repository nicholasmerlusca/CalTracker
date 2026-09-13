import CalTrack_api
from datetime import date
import database
# initialize date
today = date.today().isoformat()
def main():
    # create database
    database.init_db()
    # loop for continuous prompting
    running = True
    while running:

        meal = input("What did you eat?\n")
        # get nutrition data from API
        grams = input("How many grams/ml?\n")
        nutrition_data = CalTrack_api.get_nutrition(meal, grams)
        if nutrition_data["foods"]:
            i = 1
            print("\n nutrition info:")
            for food in nutrition_data["foods"]:
                if food['nf_brand_name'] != "N/A":
                    print(f"{i} - {food['food_name'].title()} ({food['nf_brand_name']}): "
                          f"{food['nf_calories']} kcal | "
                          f"P: {food['nf_protein']}g | "
                          f"C: {food['nf_total_carbohydrate']}g | "
                          f"F: {food['nf_total_fat']}g")
                else:
                    print(f"{i} - {food['food_name'].title()}: "
                          f"{food['nf_calories']} kcal | "
                          f"P: {food['nf_protein']}g | "
                          f"C: {food['nf_total_carbohydrate']}g | "
                          f"F: {food['nf_total_fat']}g")
                i += 1

            print(f"select listed item (by number 1-{len(nutrition_data['foods'])})")
            selection = int(input())
            if 1 <= selection <= len(nutrition_data["foods"]):
                selected_food = nutrition_data["foods"][selection - 1]
                print(f"You selected: {selected_food['food_name'].title()} ({selected_food['nf_brand_name']})")
            else:
                print("Invalid selection. Please try again.")
                continue
            print(f"would you like to log this? Y/N")
            if input().lower() == 'y':
                # update diet with each macro
                database.insert_item(selected_food["nf_calories"], selected_food["nf_protein"], selected_food["nf_total_fat"],
                                     selected_food["nf_total_carbohydrate"], selected_food["food_name"], today)
            print("Current stats for the day: \n")
            print_totals()
        else:
            print("No nutrition data found for the given food item.")
        if input("would you like to add something else? Y/N\n").lower() == 'n':
            running = False
    print("Thank you for using CalTrack!")

def print_totals():
    totals = database.get_daily_totals(today)
    print(f"Today's totals: \n"
          f"Calories: {round(totals['total_calories'], 1)} kcal\n"
          f"Protein: {round(totals['total_protein'], 1)} g\n"
          f"Fat: {round(totals['total_fat'], 1)} g\n"
          f"Carbs: {round(totals['total_carbs'], 1)} g\n")

if __name__ == '__main__':
    main()
