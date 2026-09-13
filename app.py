from flask import Flask, render_template, request, session, redirect
import CalTrack_api
import database
from datetime import date

app = Flask(__name__)
app.secret_key = "lalala"

@app.route("/", methods=["GET", "POST"])
def home():
    nutrition_data = session.get("nutrition_data", None)
    if request.method == "POST":
        action = request.form["action"]
        if action == "search":
            food = request.form["food"]
            amount = request.form["amount"]
            nutrition_data = CalTrack_api.get_nutrition(food, amount)
            session["nutrition_data"] = nutrition_data
        elif action == "log":
            choice = int(request.form.get("choice"))
            selected_food = nutrition_data["foods"][choice]
            database.insert_item(selected_food["nf_calories"], selected_food["nf_protein"], selected_food["nf_total_fat"],
                                 selected_food["nf_total_carbohydrate"], selected_food["food_name"], date.today().isoformat())
            return redirect("/")
    return render_template("index.html", name="Nick", foods=nutrition_data["foods"] if nutrition_data else [])
@app.route("/search")
def search():
    return "searching...."

if __name__ == "__main__":
    app.run()
