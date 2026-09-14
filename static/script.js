const searchForm = document.querySelector("form");

let selectedFood = null;
let selectedFoodElement = null;

const logButton = document.querySelector("#log-food");

const searchModal = document.querySelector("#search-modal");
const openSearch = document.querySelector("#open-search");
const modalBackdrop = document.querySelector("#modal-backdrop");

const circle = document.querySelector("#macro-chart");

const foodModal = document.querySelector("#food-modal");
const closeFood = document.querySelector("#close-food");
const remFood = document.querySelector("#remove-food");
let openFood = -1;

circle.style.background = "grey";

updateDailyTotals()
updateDailyEntries()

function updateDailyTotals() {
    fetch("/daily")
        .then(response => response.json())
        .then(data => {
            document.querySelector("#calories").textContent = Math.round(data["total_calories"]);
            document.querySelector("#calCirc").textContent = Math.round(data["total_calories"]);
            document.querySelector("#protein").textContent = Math.round(data["total_protein"]);
            document.querySelector("#fat").textContent = Math.round(data["total_fat"]);
            document.querySelector("#carbs").textContent = Math.round(data["total_carbs"]);

            const protCal = data["total_protein"] * 4;
            const fatCal = data["total_fat"] * 9;
            const carbCal = data["total_carbs"] * 4;
            const totalMacroCals = protCal + fatCal + carbCal;
            let protPercent;
            let fatPercent;
            let carbPercent;
            if (totalMacroCals != 0) {
                protPercent = (protCal / totalMacroCals) * 100;
                fatPercent = (fatCal / totalMacroCals) * 100;
                carbPercent = (carbCal / totalMacroCals) * 100;
                const proteinEnd = protPercent;
                const fatEnd = protPercent + fatPercent;
                const carbEnd = protPercent + fatPercent + carbPercent;
                circle.style.background = `conic-gradient(green 0% ${proteinEnd}%, red ${proteinEnd}% ${fatEnd}%, blue ${fatEnd}% ${carbEnd}%)`;

            } else {
                circle.style.background = 'grey'
            }
        });
}

function updateDailyEntries() {
    fetch("/entries")
        .then(response => response.json())
        .then(data => {
            const history = document.querySelector("#food-list");
            history.textContent = ""

            for (const food of data) {
                console.log(food);
                const foodElement = document.createElement("button");
                foodElement.textContent = food.food_name + " - " + food.calories + " kcal";
                history.appendChild(foodElement);
                foodElement.addEventListener("click", function () {
                        foodModal.classList.remove("hidden");
                        modalBackdrop.classList.remove("hidden");
                        document.querySelector("#food-calories").textContent = Math.round(food.calories);
                        document.querySelector("#food-name").textContent = food.food_name;
                        document.querySelector("#food-carbs").textContent = Math.round(food.carbs);
                        document.querySelector("#food-protein").textContent = Math.round(food.protein);
                        document.querySelector("#food-fat").textContent = Math.round(food.fat);
                        openFood = food.id;
                    }
                );
            }
        })
}

openSearch.addEventListener("click", function () {
    searchModal.classList.remove("hidden");
    modalBackdrop.classList.remove("hidden");
});

const closeSearch = document.querySelector("#close-search");
closeSearch.addEventListener("click", function () {
    searchModal.classList.add("hidden");
    modalBackdrop.classList.add("hidden");
});

logButton.addEventListener("click", function () {
    if (selectedFood == null) {
        console.log("No food selected!");
        return;
    }
    fetch("/log", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(selectedFood)

    })
        .then(response => response.text())
        .then(message => {
            const stat = document.querySelector("#status");
            stat.textContent = message;
            updateDailyTotals();
            updateDailyEntries()
            console.log(message);

        });
});

searchForm.addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(searchForm);
    fetch("/search", {
        method: "POST",
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);

            const results = document.querySelector("#search-results");

            results.textContent = "";

            for (const food of data.foods) {
                const foodElement = document.createElement("button");
                foodElement.textContent =
                    food.food_name +
                    " - " +
                    food.nf_calories +
                    " kcal, " +
                    food.nf_protein +
                    "g protein, " +
                    food.nf_total_carbohydrate +
                    "g carbs, " +
                    food.nf_total_fat +
                    "g fat";
                foodElement.addEventListener("click", function () {
                    selectedFood = food;
                    console.log("Selected food:", selectedFood);
                    if (selectedFoodElement != null) {
                        selectedFoodElement.classList.remove("selected");
                    }
                    foodElement.classList.add("selected");
                    selectedFoodElement = foodElement;
                });
                results.appendChild(foodElement);
            }
        });
});

closeFood.addEventListener("click", function () {
    foodModal.classList.add("hidden");
    modalBackdrop.classList.add("hidden");
})

remFood.addEventListener("click", function () {
    fetch("/remove", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({"id": openFood})
    })
        .then(() => {
                updateDailyTotals();
                updateDailyEntries();
                foodModal.classList.add("hidden");
                modalBackdrop.classList.add("hidden");
            }
        )
})
