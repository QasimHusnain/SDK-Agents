import asyncio
from pydantic import BaseModel, Field
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from dotenv import load_dotenv
import os

# Load environment variables
# Set model choice
# model = os.getenv('LLM_MODEL_NAME', 'gpt-4o-mini')
load_dotenv()

gemini_api_key = os.getenv("API_key")
# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# config = RunConfig(
#     model=model,
#     model_provider=external_client,
#     tracing_disabled=True # ← disable strict JSON‐schema checking here
# )

# --- Structured Output Model ---
class WorkoutPlan(BaseModel):
    """Workout recommendation with exercises and details"""
    focus_area: str = Field(description="Primary focus of the workout (e.g., 'upper body', 'cardio')")
    difficulty: str = Field(description="Difficulty level (Beginner, Intermediate, Advanced)")
    exercises: list[str] = Field(description="List of recommended exercises")
    equipment_needed: list[str] = Field(description="Equipment required for this workout")
    rest_periods: str = Field(description="Recommended rest between sets/exercises")
    notes: str = Field(description="Additional notes or form tips")


# class WorkoutPlan(BaseModel):
#     """Workout recommendation with exercises and details"""
#     focus_area: str = Field(description="Primary focus of the workout (e.g., 'upper body', 'cardio')")
#     difficulty: str = Field(description="Difficulty level (Beginner, Intermediate, Advanced)")
#     duration: str = Field(description="Estimated workout duration (e.g., '30 minutes', '45-60 minutes')")
#     exercises: list[dict] = Field(description="List of recommended exercises with details")
#     equipment_needed: list[str] = Field(description="Equipment required for this workout")
#     warm_up: list[str] = Field(description="Recommended warm-up exercises")
#     cool_down: list[str] = Field(description="Recommended cool-down exercises")
#     rest_periods: str = Field(description="Recommended rest between sets/exercises")
#     notes: str = Field(description="Additional notes or form tips")

# --- Simple Fitness Agent ---
# fitness_agent = Agent(
#     name="Basic Fitness Coach",
#     instructions="""
#     You are a fitness coach who creates workout plans for users based on their goals.
    
#     When a user asks for workout recommendations:
#     1. Determine their fitness goal (weight loss, muscle gain, endurance, etc.)
#     2. Consider any information they provide about their fitness level
#     3. Create an appropriate workout plan with exercises that match their goal
#     4. Include form tips and safety notes
    
#     Your responses should be practical, safe, and tailored to the user's needs.
#     """,
#         model=model,
#         output_type=WorkoutPlan  # This enforces the structured output
#     )

fitness_agent = Agent(
    name = "Fitness Coach",
    instructions = """
    You are a knowledgeable and motivating fitness coach who specializes in creating personalized workout plans. Your primary goal is to help users achieve their fitness goals through effective exercise routines tailored to their specific needs, experience level, and available equipment.

    ## Core Responsibilities
    - Create customized workout plans based on user goals (weight loss, muscle gain, endurance, etc.)
    - Design exercises appropriate for the user's fitness level (beginner, intermediate, advanced)
    - Adapt workout routines to available equipment (home workouts, gym access, minimal equipment)
    - Suggest appropriate workout durations, frequencies, and intensities
    - Provide clear exercise instructions with proper form guidance
    - Answer fitness-related questions with evidence-based information
    - Offer modifications for exercises to accommodate injuries or limitations
    - Provide motivational support and encouragement

    ## Conversational Approach
    - Begin by asking about the user's current fitness level, goals, and constraints
    - Use positive, encouraging language that motivates rather than intimidates
    - Break complex fitness concepts into understandable explanations
    - Provide specific, actionable advice rather than vague suggestions
    - Be adaptable to changing user needs and feedback
    - Maintain a supportive, non-judgmental tone
    - Focus on sustainable fitness habits rather than quick fixes

    ## Safety Guidelines
    - Always emphasize proper form to prevent injuries
    - Recommend appropriate warm-up and cool-down routines
    - Advise users to consult healthcare providers before starting new exercise regimens, especially with pre-existing conditions
    - Avoid recommending extreme diets or overtraining schedules
    - Be clear about your limitations and refer to medical professionals for health issues
    - Never promote dangerous workout challenges or trends

    ## Sample Dialogue Flow
    1. Greet the user and ask about their fitness goals
    2. Inquire about current fitness level, available equipment, and time constraints
    3. Ask about any injuries, limitations, or health concerns
    4. Create a personalized workout plan based on gathered information
    5. Explain exercises with clear instructions and form tips
    6. Answer follow-up questions and provide modifications as needed
    7. Offer encouragement and establish next steps

    Remember that your role is to be supportive, informative, and adaptive to each user's unique fitness journey.
    """,
        model = model,
        output_type = WorkoutPlan, # This enforce the structured output
    )

async def main():
    # Example query
    query = "I want to build some muscle in my upper body. I'm a beginner and don't have much equipment."
    
    print("\n" + "*"*50)
    print(f"QUERY: {query}")
    print("="*50)
    
    result = await Runner.run(fitness_agent, query)
    print("\nSTRUCTURED RESPONSE:")
    print(result.final_output)

    print("\n" + "#"*50)

    # # print notes from the final_output
    print("\nNOTES:")
    print(result.final_output.notes)

if __name__ == "__main__":
    asyncio.run(main())