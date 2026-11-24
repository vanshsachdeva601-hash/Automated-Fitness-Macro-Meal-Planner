import csv
import matplotlib.pyplot as plt

# Function 1: User Details Input & Validation
def get_user_details():
    print("--- AUTOMATED FITNESS AND MEAL PLANNER ---")
    name = input("Enter your name: ")

    # Age input check
    while True:
        try:
            age = int(input("Enter your age: "))
            if age > 0:
                break
            else:
                print("Age must be positive!")
        except:
            print("Please enter a valid number for age.")

    # Weight input check
    while True:
        try:
            weight = float(input("Enter your weight in kg: "))
            if weight > 0:
                break
            else:
                print("Weight must be positive!")
        except:
            print("Please enter a valid number for weight.")

    # Height input check
    while True:
        try:
            height = float(input("Enter your height in cm: "))
            if height > 0:
                break
            else:
                print("Height must be positive!")
        except:
            print("Please enter a valid number for height.")

    # Gender choice
    while True:
        gender = input("Enter gender (male/female): ").lower().strip()
        if gender == "male" or gender == "female":
            break
        print("Please enter either male or female.")

    # Activity level selection
    print("\nSelect your activity level:")
    print("1. Sedentary (Little or no exercise)")
    print("2. Lightly Active (Exercise 1-3 days/week)")
    print("3. Moderately Active (Exercise 3-5 days/week)")
    print("4. Very Active (Exercise 6-7 days/week)")

    while True:
        act_choice = input("Enter option (1-4): ")
        if act_choice == "1":
            activity_multiplier = 1.2
            break
        elif act_choice == "2":
            activity_multiplier = 1.375
            break
        elif act_choice == "3":
            activity_multiplier = 1.55
            break
        elif act_choice == "4":
            activity_multiplier = 1.725
            break
        else:
            print("Invalid option! Enter 1, 2, 3, or 4.")

    # Goal selection
    print("\nSelect your fitness goal:")
    print("1. Weight Loss")
    print("2. Weight Maintenance")
    print("3. Muscle Gain")

    while True:
        goal_choice = input("Enter option (1-3): ")
        if goal_choice == "1" or goal_choice == "2" or goal_choice == "3":
            break
        print("Invalid choice! Enter 1, 2, or 3.")

    return name, age, weight, height, gender, activity_multiplier, goal_choice



# Function 2: Calorie & Macro Calculations

def calculate_calories(age, weight, height, gender, activity_multiplier, goal_choice):
    # BMR formula (Mifflin-St Jeor)
    if gender == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # TDEE = BMR * Activity Level
    tdee = bmr * activity_multiplier

    # Target calories adjustment based on goal
    if goal_choice == "1":
        target_calories = tdee - 500  # Deficit for weight loss
    elif goal_choice == "3":
        target_calories = tdee + 300  # Surplus for muscle gain
    else:
        target_calories = tdee  # Maintenance

    # Target Macros (30% Protein, 50% Carbs, 20% Fats)
    # 1g Protein = 4 cal, 1g Carb = 4 cal, 1g Fat = 9 cal
    target_protein = (target_calories * 0.30) / 4
    target_carbs = (target_calories * 0.50) / 4
    target_fats = (target_calories * 0.20) / 9

    return bmr, tdee, target_calories, target_protein, target_carbs, target_fats



# Function 3: Reading CSV File Data

def read_food_data(file_name):
    food_list = []
    try:
        f = open(file_name, "r")
        reader = csv.reader(f)
        header = next(reader)  # Skip the column names row

        for row in reader:
            if len(row) >= 7:
                item = {
                    "name": row[0],
                    "type": row[1],
                    "calories": float(row[2]),
                    "protein": float(row[3]),
                    "carbs": float(row[4]),
                    "fats": float(row[5]),
                    "category": row[6]
                }
                food_list.append(item)
        f.close()
    except:
        print("Error: Could not read the CSV file!")

    return food_list



# Function 4: Finding Best Meal Combination

def find_best_meals(food_list, target_calories):
    breakfasts = []
    lunches = []
    dinners = []
    snacks = []

    # Separate items by meal type using standard loops
    for item in food_list:
        if item["type"] == "Breakfast":
            breakfasts.append(item)
        elif item["type"] == "Lunch":
            lunches.append(item)
        elif item["type"] == "Dinner":
            dinners.append(item)
        elif item["type"] == "Snack":
            snacks.append(item)

    best_combo = None
    min_diff = 100000  # Starting with a large difference number

    # Simple nested loops to check combinations
    for b in breakfasts:
        for l in lunches:
            for d in dinners:
                for s in snacks:
                    total_cal = b["calories"] + l["calories"] + d["calories"] + s["calories"]
                    diff = abs(total_cal - target_calories)

                    if diff < min_diff:
                        min_diff = diff
                        best_combo = [b, l, d, s, total_cal]

    return best_combo



# Function 5: Matplotlib Pie Chart

def show_pie_chart(protein, carbs, fats):
    labels = ['Protein', 'Carbs', 'Fats']
    amounts = [protein, carbs, fats]

    plt.figure()
    plt.pie(amounts, labels=labels, autopct='%1.1f%%')
    plt.title("Macronutrient Breakdown (in grams)")
    plt.show()



# Main Function

def main():
    # Step 1: Get inputs
    name, age, weight, height, gender, act_mult, goal_choice = get_user_details()

    # Step 2: Calculate targets
    bmr, tdee, target_cal, target_p, target_c, target_f = calculate_calories(
        age, weight, height, gender, act_mult, goal_choice
    )

    # Step 3: Load data
    food_data = read_food_data("food_database.csv")
    if len(food_data) == 0:
        print("No food data available!")
        return

    # Step 4: Find meals
    result = find_best_meals(food_data, target_cal)

    # Step 5: Print Summary
    if result != None:
        b = result[0]
        l = result[1]
        d = result[2]
        s = result[3]
        total_cal = result[4]

        total_p = b["protein"] + l["protein"] + d["protein"] + s["protein"]
        total_c = b["carbs"] + l["carbs"] + d["carbs"] + s["carbs"]
        total_f = b["fats"] + l["fats"] + d["fats"] + s["fats"]

        print("\n-------------------------------------------")
        print("FINAL MEAL PLAN FOR:", name)
        print("-------------------------------------------")
        print("Your BMR:", round(bmr, 2), "kcal")
        print("Your TDEE:", round(tdee, 2), "kcal")
        print("Target Daily Calories:", round(target_cal, 2), "kcal")
        print("Total Plan Calories:", round(total_cal, 2), "kcal")
        print("-------------------------------------------")
        print("MEAL SUGGESTIONS:")
        print("Breakfast :", b["name"], "(", b["calories"], "kcal )")
        print("Lunch :", l["name"], "(", l["calories"], "kcal )")
        print("Dinner :", d["name"], "(", d["calories"], "kcal )")
        print("Snack :", s["name"], "(", s["calories"], "kcal )")
        print("-------------------------------------------")
        print("MACROS BREAKDOWN:")
        print("Protein :", round(total_p, 1), "g (Target:", round(target_p, 1), "g)")
        print("Carbs :", round(total_c, 1), "g (Target:", round(target_c, 1), "g)")
        print("Fats :", round(total_f, 1), "g (Target:", round(target_f, 1), "g)")
        print("-------------------------------------------")

        # Step 6: Show chart
        show_pie_chart(total_p, total_c, total_f)


# Start the program
main()