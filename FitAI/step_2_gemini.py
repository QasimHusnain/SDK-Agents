# Importing necessary modules for the script
import os  # Provides functions to interact with the operating system
import json  # Enables working with JSON data
import asyncio  # Supports asynchronous programming
from dotenv import load_dotenv  # Loads environment variables from a .env file
import google.generativeai as genai  # Imports Google's Generative AI library

# Load environment variables from the .env file
load_dotenv()  # Loads variables from .env into the environment

# Retrieve the API key for Gemini from environment variables
gemini_api_key = os.getenv("API_key")  # Fetches the API key from environment

# Check if the API key is available; raise an error if not
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please check your .env file.")

# Configure the Gemini API with the retrieved API key
genai.configure(api_key=gemini_api_key)  # Sets up the API key for authentication

# Initialize the Gemini Generative Model with a specific version
model = genai.GenerativeModel("gemini-2.0-flash")  # Creates an instance of the model

# Define a function to get exercise information based on muscle group
def get_exercise_info(muscle_group: str) -> dict:
    """
    Returns a list of exercises for the specified muscle group.
    """
    # Dictionary containing exercises for different muscle groups
    data = {
        "chest": [
            "Push-ups: 3 sets of 10-15 reps",
            "Bench Press: 3 sets of 8-12 reps",
            "Chest Flyes: 4 sets of 12-15 reps",
            "Incline Push-ups: 3 sets of 10-15 reps"
        ],
        "back": [
            "Pull-ups: 3 sets of 6-10 reps",
            "Bent-over Rows: 3 sets of 8-12 reps",
            "Lat Pulldowns: 3 sets of 10-12 reps",
            "Superman Holds: 3 sets of 30 seconds"
        ],
        "legs": [
            "Squats: 3 sets of 10-15 reps",
            "Lunges: 3 sets of 10 per leg",
            "Calf Raises: 3 sets of 15-20 reps",
            "Glute Bridges: 3 sets of 15 reps"
        ],
        "arms": [
            "Bicep Curls: 3 sets of 10-12 reps",
            "Tricep Dips: 3 sets of 10-15 reps",
            "Hammer Curls: 3 sets of 10-12 reps",
            "Overhead Tricep Extensions: 3 sets of 10-12 reps"
        ],
        "core": [
            "Planks: 3 sets of 30-60 seconds",
            "Crunches: 3 sets of 15-20 reps",
            "Russian Twists: 3 sets of 20 total reps",
            "Mountain Climbers: 3 sets of 20 total reps"
        ]
    }
    # Return exercises for the specified muscle group; default message if not found
    return data.get(muscle_group.lower(), ["No data available for this group."])

# Define a function to calculate daily calorie needs and macronutrient breakdown
def calculate_calories(goal: str, weight: float, height: float, age: int, gender: str) -> dict:
    """
    Calculates daily calorie requirements and macronutrient distribution
    based on user's goal, weight, height, age, and gender.
    """
    # Calculate Basal Metabolic Rate (BMR) using Mifflin-St Jeor Equation
    if gender.lower() in ["male", "m"]:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    # Estimate Total Daily Energy Expenditure (TDEE) assuming moderate activity
    tdee = bmr * 1.55

    # Adjust calorie target and macronutrient ratios based on the user's goal
    if goal == "weight loss":
        calorie_target = tdee - 500  # Create a calorie deficit
        macros = (0.40, 0.30, 0.30)  # Protein, Fat, Carbs ratios
    elif goal == "muscle gain":
        calorie_target = tdee + 300  # Create a calorie surplus
        macros = (0.30, 0.25, 0.45)  # Protein, Fat, Carbs ratios
    else:
        calorie_target = tdee  # Maintain current weight
        macros = (0.30, 0.30, 0.40)  # Protein, Fat, Carbs ratios

    # Calculate grams of each macronutrient based on calorie target
    protein_grams = round((calorie_target * macros[0]) / 4)  # 4 kcal per gram of protein
    fat_grams = round((calorie_target * macros[1]) / 9)      # 9 kcal per gram of fat
    carb_grams = round((calorie_target * macros[2]) / 4)     # 4 kcal per gram of carbohydrate

    # Return the calculated daily calories and macronutrient breakdown
    return {
        "daily_calories": round(calorie_target),
        "macros": {
            "protein": protein_grams,
            "fat": fat_grams,
            "carbs": carb_grams
        }
    }

# Define an asynchronous function to interact with the Gemini model
async def chat_with_gemini(prompt: str) -> str:
    """
    Sends a prompt to the Gemini model and returns the generated response.
    """
    response = model.generate_content(prompt)  # Generate response from the model
    return response.text  # Return the text content of the response

# Define the main asynchronous function to handle user queries
async def main():
    """
    Processes a list of user queries and provides appropriate responses.
    """
    # List of sample queries to process
    queries = [
        "What are some good leg exercises I can do at home without tools?",
        "I'm 30 years old, male, 175cm tall, and weigh 80kg. How many calories should I eat to lose weight?",
        "guide about nutrition fit for me"
    ]

    # Iterate through each query in the list
    for query in queries:
        print("\n" + "#"*50)  # Print a separator line
        print(f"QUERY: {query}\n" + "="*50)  # Display the current query

        # Check if the query is related to exercises
        if "exercise" in query.lower() or "chest" in query.lower():
            exercises = get_exercise_info("chest")  # Get chest exercises
            output = f"Here are recommended chest exercises:\n" + "\n".join(exercises)
        # Check if the query is related to calorie calculation
        elif "calories" in query.lower():
            nutrition = calculate_calories("weight loss", 80, 175, 30, "male")  # Calculate nutrition info
            output = f"Daily Calorie Needs: {nutrition['daily_calories']} kcal\n"
            output += "Macronutrient Breakdown:\n"
            output += f"- Protein: {nutrition['macros']['protein']}g\n"
            output += f"- Fat: {nutrition['macros']['fat']}g\n"
            output += f"- Carbs: {nutrition['macros']['carbs']}g\n"
        # For other queries, use the Gemini model to generate a response
        else:
            output = await chat_with_gemini(query)  # Get response from Gemini model

        print("RESPONSE:\n" + output)  # Display the response

# Entry point of the script
if __name__ == "__main__":
    asyncio.run(main())  # Run the main asynchronous function
 
