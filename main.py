import requests
import csv

app_id = ""  # Your Edamam app ID
app_key = ""  # Your Edamam app key

csv_file = "recipes.csv"

# Create and format CSV file
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Recipe Name", "Ingredients", "URL", "Calories", "Diet Labels", "Meal Type"])

diet_types = {
    "balanced": "Balanced",
    "high-protein": "High Protein",
    "low-fat": "Low Fat",
    "low-carb": "Low Carb",
    "high-fiber": "High Fiber",
    "low-sodium": "Low Sodium"
}

meal_types = {
    "breakfast": "Breakfast",
    "lunch/dinner": "Lunch/Dinner",
    "snack": "Snack"
}

def get_preferences():
    ingredient = input("Enter an ingredient: ").strip()

    print("\nChoose a diet type:")
    for value in diet_types.values():
        print(f"- {value}")
    diet_type = input("Enter preferred diet type or press Enter to skip: ").strip().lower()

    print("\nChoose a meal type:")
    for value in meal_types.values():
        print(f"- {value}")
    meal_type = input("Enter preferred meal type or press Enter to skip: ").strip().lower()

    return ingredient, diet_type, meal_type

def search(ingredient, diet_type, meal_type):
    url = f"https://api.edamam.com/api/recipes/v2?type=public&q={ingredient}&app_id={app_id}&app_key={app_key}"

    if diet_type in diet_types:
        url += f"&diet={diet_type}"
    if meal_type in meal_types:
        url += f"&mealType={meal_type}"

    headers = {"Edamam-Account-User": ""} # Your Edamam account user ID
    result = requests.get(url, headers=headers)
    data = result.json()
    recipes = data.get("hits", [])

    if not recipes:
        print("\nNo recipes found.")
        print(f"API URL used: {url}")
        return

    print("\nRecipes Found:")
    for i, recipe in enumerate(recipes, start=1):
        info = recipe["recipe"]
        print(f"{i}. {info['label']}\nURL: {info['url']}\n")

    with open(csv_file, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for recipe in recipes:
            info = recipe["recipe"]
            writer.writerow([
                info["label"],
                ", ".join(info.get("ingredientLines", [])),
                info["url"],
                round(info["calories"], 2),
                ", ".join(info.get("dietLabels", [])),
                ", ".join(info.get("mealType", []))
            ])
    print(f"\nRecipes saved to '{csv_file}'")

def main():
    ingredient, diet_type, meal_type = get_preferences()
    search(ingredient, diet_type, meal_type)

if __name__ == "__main__":
    main()
