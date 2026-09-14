# CalTrack

CalTrack is a nutrition tracking web app I've built with Python and Flask.

The goal is to make it easy to search for food, log what I eat, and keep track of my daily calories and macros.

## Features

* Search for foods using the USDA FoodData Central API
* Enter the amount of food in grams/ml
* View calories, protein, fat, and carbs
* Log foods to a SQLite database
* View today's logged foods
* Remove foods from the daily log
* Track daily calorie and macro totals
* View protein, fat, and carb ratios with a donut chart

## Built With

* Python
* Flask
* JavaScript
* HTML/CSS
* SQLite
* USDA FoodData Central API


## Running Locally

Clone the repository:

```bash
git clone https://github.com/nicholasmerlusca/CalTracker.git
cd CalTrack
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install the required packages:

```bash
pip install flask requests python-dotenv
```

Create a `.env` file and add your API key:

```env
API_KEY=your_api_key
SECRET_CODE=your_secret_key
```

Then run:

```bash
python app.py
```

Open the local Flask address in your browser.

## Future Plans

* Add macro goals
* Add editing for already logged food
* Better error handling
* Possibly deploy the application
