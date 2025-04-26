import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel


load_dotenv()

gemini_api_key = os.getenv("API_key")

Provider = AsyncOpenAI(api_key=gemini_api_key,
base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
) 

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
   openai_client=Provider
)

greet_agent = Agent(
    name="Greeting Agent",
    instructions = """You are a greeting agent. You are responsible for greeting the user with frinedly message.When Someone says, Hi or hello, Greet with Salam from Qasim Husnain.
    If someone says bye or goodbye,Greet with Allah Hafiz from Qasim Husnain.
    if someone says anything else, Say, I am sorry, I just do greetings. """,
    model=model,
    tools=[]
)

# result = Runner.run_sync(greet_agent, "by")
# print(result.final_output)

# I want to get input from user in terminal to make it more easy.
user_input = input("Please enter your question: ")
result = Runner.run_sync(greet_agent, user_input)
print(result.final_output)






