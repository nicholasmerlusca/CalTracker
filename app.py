from flask import Flask, render_template, request, redirect, jsonify
import CalTrack_api
import database
from datetime import date
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_CODE")
today = date.today().isoformat()

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html", name="Nick")
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        food = request.form["food"]
        amount = request.form["amount"]
        nutrition_data = CalTrack_api.get_nutrition(food, amount)
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
    tot = database.get_daily_totals(today)
    return jsonify(dict(tot))

@app.route("/entries", methods=["GET"])
def entries():
    tot = database.get_daily_entries(today)
    lst = []
    for entry in tot:
        lst.append(dict(entry))

    return jsonify(lst)

@app.route("/remove", methods=["POST"])
def remove():
    food = request.get_json()
    database.remove_item(food['id'])
    return



if __name__ == "__main__":
    app.run()
