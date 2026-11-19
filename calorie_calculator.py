# MIT License
#
# Copyright (c) 2026 Diego, Dario, Fan, Javier, José Luis and Sebas
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Daily Calorie and Protein Calculator.
Calculates how many calories and how much protein a person needs
per day, based on body data, activity level and goal.
No external libraries are needed.
"""

# Activity factors used to multiply the BMR
ACTIVITY_FACTORS = {"low": 1.2, "moderate": 1.55, "high": 1.725}

# Calories added or subtracted depending on the goal
GOAL_ADJUSTMENTS = {"lose": -300, "maintain": 0, "gain": 300}

# Safety floor: the program never recommends less than this
MIN_CALORIES = 1200

# Grams of protein per kg of body weight, depending on the goal
PROTEIN_FACTORS = {"lose": 2.2, "maintain": 1.6, "gain": 2.0}

# Energy in 1 gram of protein (kcal)
KCAL_PER_GRAM_PROTEIN = 4


# Member 1
def get_user_data() -> dict:
    """
    Ask the user for their data, validate it and return it.
    Returns:
        dict: {"weight", "height", "age", "sex", "activity_level", "goal"}
    Example:
        Input typed: 70, 175, 19, male, moderate, gain
        Output: {"weight": 70.0, "height": 175.0, "age": 19, "sex": "male",
                 "activity_level": "moderate", "goal": "gain"}
    """
    weight = float(input("Weight (kg): "))
    height = float(input("Height (cm): "))
    age = int(input("Age (years): "))
    sex = input("Sex (male/female): ").strip().lower()
    activity_level = input("Activity level (low/moderate/high): ").strip().lower()
    goal = input("Goal (lose/maintain/gain): ").strip().lower()

    # Numbers must be positive and inside reasonable limits
    if weight <= 0 or height <= 0 or age <= 0:
        raise ValueError("Weight, height and age must be positive numbers.")
    if not (30 <= weight <= 300 and 100 <= height <= 250 and 14 <= age <= 100):
        raise ValueError("Weight, height or age out of range.")

    # Text values must be one of the allowed options
    if sex not in ("male", "female"):
        raise ValueError("Sex must be 'male' or 'female'.")
    if activity_level not in ACTIVITY_FACTORS:
        raise ValueError("Activity level must be 'low', 'moderate' or 'high'.")
    if goal not in GOAL_ADJUSTMENTS:
        raise ValueError("Goal must be 'lose', 'maintain' or 'gain'.")

    return {
        "weight": weight,
        "height": height,
        "age": age,
        "sex": sex,
        "activity_level": activity_level,
        "goal": goal,
    }


# Member 2
def calculate_bmr(weight: float, height: float, age: int, sex: str) -> float:
    """
    Calculate the Basal Metabolic Rate (Mifflin-St Jeor formula).
    Returns:
        float: Calories burned at rest per day (kcal).
    Example:
        calculate_bmr(70, 175, 19, "male") -> 1703.75
    """
    # Common part of the formula for both sexes
    bmr = 10 * weight + 6.25 * height - 5 * age

    # Men add 5, women subtract 161
    if sex == "male":
        bmr += 5
    else:
        bmr -= 161

    return bmr


# Member 3
def apply_activity(bmr: float, activity_level: str) -> float:
    """
    Multiply the BMR by the activity factor to get the TDEE
    (Total Daily Energy Expenditure).
    Example:
        apply_activity(1703.75, "moderate") -> 2640.8125
    """
    factor = ACTIVITY_FACTORS[activity_level]
    tdee = bmr * factor
    return tdee


# Member 4
def adjust_for_goal(tdee: float, goal: str) -> float:
    """
    Adjust the daily calories depending on the goal,
    never going below the safety floor (MIN_CALORIES).
    Example:
        adjust_for_goal(2640.8125, "gain") -> 2940.8125
        adjust_for_goal(1400, "lose")      -> 1200 (floor applied)
    """
    adjustment = GOAL_ADJUSTMENTS[goal]
    calories = tdee + adjustment

    # Safety floor: eating too little is not healthy
    if calories < MIN_CALORIES:
        calories = MIN_CALORIES

    return calories


# Member 5
def calculate_protein(weight: float, goal: str) -> float:
    """
    Calculate the daily protein needed using a goal-specific factor
    (lose: 2.2 g/kg, maintain: 1.6 g/kg, gain: 2.0 g/kg).
    Example:
        calculate_protein(70, "gain") -> 140.0
    """
    factor = PROTEIN_FACTORS[goal]
    protein = weight * factor
    return protein


# Member 6
def format_result(calories: float, protein: float, goal: str) -> str:
    """
    Split the calories into protein and the rest (carbs and fats),
    and return a formatted summary.
    Example:
        format_result(2940.8125, 140.0, "gain") -> summary with
        2941 kcal, 140 g protein, 560 kcal protein, 2381 kcal remaining
    """
    protein_kcal = protein * KCAL_PER_GRAM_PROTEIN
    remaining_kcal = calories - protein_kcal

    return (
        f"--- Daily plan (goal: {goal}) ---\n"
        f"Calories:              {round(calories)} kcal/day\n"
        f"Protein:               {round(protein)} g/day\n"
        f"Calories from protein: {round(protein_kcal)} kcal\n"
        f"Left for carbs & fats: {round(remaining_kcal)} kcal"
    )


def main() -> None:
    """Run the full program: read data, calculate and show the result."""
    data = get_user_data()
    bmr = calculate_bmr(data["weight"], data["height"], data["age"], data["sex"])
    tdee = apply_activity(bmr, data["activity_level"])
    calories = adjust_for_goal(tdee, data["goal"])
    protein = calculate_protein(data["weight"], data["goal"])
    print(format_result(calories, protein, data["goal"]))


if __name__ == "__main__":
    main()
