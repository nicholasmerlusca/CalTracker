from flask import Flask, render_template, request, session, redirect, jsonify
import CalTrack_api
import database
from datetime import date


app = Flask(__name__)
app.secret_key = "lalala"

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html", name="Nick")
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        food = request.form["food"]
        amount = request.form["amount"]
        nutrition_data = CalTrack_api.get_nutrition(food, amount)
        session["nutrition_data"] = nutrition_data
        return jsonify(nutrition_data)
    return "Search requires POST"

@app.route("/log", methods=["POST"])
def log():
    selected_food = request.get_json()
    database.insert_item(selected_food["nf_calories"], selected_food["nf_protein"], selected_food["nf_total_fat"],
                         selected_food["nf_total_carbohydrate"], selected_food["food_name"], date.today().isoformat())
    return "logged successfully"

@app.route("/daily", methods=["GET"])
def daily():
    today = date.today().isoformat()
    tot = database.get_daily_totals(today)
    return jsonify(dict(tot))



if __name__ == "__main__":
    app.run()
