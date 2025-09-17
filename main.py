import CalTrack_api
from datetime import date
import csv
import os
# initialize date
today = date.today().isoformat()
def main():
    # create or fetch diet dictionary
    diet = {'date': today, "calories": 0.0, "protein": 0.0, "fat": 0.0, "carbs": 0.0}
    if os.path.exists('diet_history.csv'):
        get_daily_diet()
    # loop for continuous prompting
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
                # update diet with each macro
                for food in nutrition_data["foods"]:
                    diet["calories"] += food["nf_calories"]
                    diet["protein"] += food["nf_protein"]
                    diet["fat"] += food["nf_total_fat"]
                    diet["carbs"] += food["nf_total_carbohydrate"]
            print("Current stats for the day: \n")
            print_diet(diet)
        if input("would you like to add something else? Y/N\n").lower() == 'n':
            running = False
    print("saving diet...")
    update_history(diet)
    print("Thank you for using CalTrack!")


def print_diet(diet):
    for macro in diet:
        if macro == 'date':
            print(f'{macro}:  {(diet[macro])}')
        else:
            print(f'{macro}: {round(diet[macro], 2)}')

def get_daily_diet():
    with open('diet_history.csv', 'r', newline= '') as csvfile:
        for row in csv.reader(csvfile):
            if row[0] == today:
                diet = {'date': today, "calories": row[1], "protein": row[2], "fat": row[3], "carbs": row[4]}
    return None

def update_history(diet):
    data = []
    if os.path.exists('diet_history.csv'):
            with open('diet_history.csv', 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    data.append(row)
            for i in range(len(data)):
                if data[i][0] == today:
                    data[i] = [diet['date'], diet['calories'], diet['protein'], diet['fat'], diet['carbs']]
                    break
                else:
                    data.append(diet)
            with open('diet_history.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(data)
    else:
        with open('diet_history.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([diet['date'], diet['calories'], diet['protein'], diet['fat'], diet['carbs']])


if __name__ == '__main__':
    main()
