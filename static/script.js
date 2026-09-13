const searchForm = document.querySelector("form");

let selectedFood = null;
let selectedFoodElement = null;

const logButton = document.querySelector("#log-food");

const searchModal = document.querySelector("#search-modal");
const openSearch = document.querySelector("#open-search");
const modalBackdrop = document.querySelector("#modal-backdrop");

openSearch.addEventListener("click", function() {
    searchModal.classList.remove("hidden");
    modalBackdrop.classList.remove("hidden");
});

const closeSearch = document.querySelector("#close-search");
closeSearch.addEventListener("click", function() {
    searchModal.classList.add("hidden");
    modalBackdrop.classList.add("hidden");
});

logButton.addEventListener("click", function() {
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
            console.log(message);

        });
});

searchForm.addEventListener("submit", function(event) {
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
                foodElement.addEventListener("click", function() {
                    selectedFood = food;
                    console.log("Selected food:", selectedFood);
                    if (selectedFoodElement != null){
                        selectedFoodElement.classList.remove("selected");
                    }
                    foodElement.classList.add("selected");
                    selectedFoodElement = foodElement;
                });
                results.appendChild(foodElement);
            }
        });
});
