# DETAILS:
#   title: AI Chatbot
#   author: Andrew Seamana
#   date: 2026-09-23
#
#



# Copied from: 'https://byuidatascience.github.io/agentic_ai_course/lessons/lesson1_4.html'
# def get_response(prompt: str) -> str:
#     return prompt

# def main():
#     while True:
#         try:
#             prompt = input("Input: ")
#             if prompt == "exit": break
#             response = get_response(prompt)
#         except EOFError:
#             break
#         print(response)

# if __name__ == "__main__":
#     main()



# Copied from: Took code (commented out) from `Example1_2.ipynb` and AI changed.
#
# import os
# from google.colab import userdata
# os.environ["GOOGLE_API_KEY"] = userdata.get("GOOGLE_API_KEY")
#
import os
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("GEMINI_API_KEY"):
    raise RuntimeError("GOOGLE_API_KEY is not set")



# Copied from: 'https://docs.langchain.com/oss/python/langchain/overview'
from langchain.agents import create_agent

# Idea: Perhaps I could set up a function called `pull_weather_data` or something and provide to the tool as a function call it can use to pull the data for the user provided city (input) and restate the data as a more user-friendly output.

from openmeteopy import openmeteopy

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    weather = openmeteopy.get_weather(city)
    return f" {city}!"

agent = create_agent(
    model="google_genai:gemini-3.6-flash",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# (Line copied from `Example1_2.ipynb`)
from langchain.messages import HumanMessage

prompt = HumanMessage(input("Input: "))

result = agent.invoke(
    {"messages": [{f"role": "user", "content": "What's the weather in {prompt.content}?"}]}
)

# print(result["messages"][-1].content_blocks)
print(result["messages"][-1].text) # swapped `.content_blocks` for `.text`






