# Daily Calorie & Protein Calculator

A simple Python command-line tool that calculates how many calories and how much protein a person needs per day, based on body data, activity level and goal.

Project for *Professional Skills for Engineers* (ULPGC).

## How it works

1. `get_user_data()` reads and checks the six inputs.
2. `calculate_bmr()` uses the Mifflin-St Jeor formula.
3. `apply_activity()` multiplies the BMR by the activity factor (1.2 / 1.55 / 1.725).
4. `adjust_for_goal()` adds −300, 0 or +300 kcal, with a minimum of 1200 kcal.
5. `calculate_protein()` uses 2.2, 1.6 or 2.0 g of protein per kg, depending on the goal.
6. `format_result()` splits the calories into protein and carbs & fats.

No external libraries are needed.

## How to run

```bash
python calorie_calculator.py
```

Example: male, 70 kg, 175 cm, 19 years, moderate, gain → **2941 kcal/day** and **140 g protein/day**.

## Authors

Diego, Dario, Fan, Javier, José Luis and Sebas.

## License

MIT License. See [LICENSE](LICENSE).
