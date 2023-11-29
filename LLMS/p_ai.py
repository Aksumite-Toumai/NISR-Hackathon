# https://pypi.org/project/pandasai/
import os
from dotenv import load_dotenv
import pandas as pd
from pandasai.llm.openai import OpenAI
# from pandasai import PandasAI
from pandasai import SmartDataframe

# Load environment variables
load_dotenv()

# Retrieve OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

def chat_with_csv(df, query):
    llm = OpenAI(model="gpt-4-1106-preview")
    df = SmartDataframe(df, config={"llm": llm})
    result = df.chat(query)

    return result

df = pd.read_csv("NIMC.csv")
query = input("Enter your query: ")
result = chat_with_csv(df, query)
print(result)
