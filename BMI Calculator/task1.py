"""
A Friendly Command-Line BMI Calculator
---------------------------------------

"""

def get_positive_number(message):
    """Keep asking until the user gives a valid positive number."""
    while True:
        try:
            value = float(input(message))
            if value <= 0:
                print("That number seems impossible... try again!")
                continue
            return value
        except ValueError:
            print("Oops, that's not a number. Try again!")


def calculate_bmi(weight_kg, height_m):
    return weight_kg / (height_m ** 2)


def get_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"
    


def draw_gauge(bmi):
    """A tiny ASCII gauge from 10 to 40 BMI."""
    scale_min, scale_max, width = 10, 40, 30
    position = int((bmi - scale_min) / (scale_max - scale_min) * width)
    position = max(0, min(width, position))  # keep it on the bar
    bar = "-" * position + "O" + "-" * (width - position)
    return f"[{bar}]"


def main():
    print("-" * 50)
    print(" WELCOME TO THE BMI CALCULATOR ")
    print("-" * 50)

    while True:
        unit_choice = input("\nUse (1) Metric [kg/m] or (2) Imperial [lb/in]? ").strip()

        if unit_choice == "1":
            weight = get_positive_number("Enter your weight in kg: ")
            height = get_positive_number("Enter your height in meters (e.g. 1.75): ")
        elif unit_choice == "2":
            weight_lb = get_positive_number("Enter your weight in pounds: ")
            height_in = get_positive_number("Enter your height in inches: ")
            weight = weight_lb * 0.453592
            height = height_in * 0.0254
        else:
            print("Please choose either 1 or 2.")
            continue

        bmi = calculate_bmi(weight, height)
        category = get_category(bmi)

        print("\n" + "-" * 50)
        print(f"Your BMI is: {bmi:.1f}")
        print(f"Category: {category}")
        print(draw_gauge(bmi))
        print("-" * 50)

        again = input("\nCalculate another BMI? (y/n): ").strip().lower()
        if again != "y":
            print("\nThanks for using the BMI Calculator. Stay healthy!")
            break


if __name__ == "__main__":
    main()