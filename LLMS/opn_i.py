from openai import OpenAI
from dotenv import load_dotenv
import os
import pandas as pd
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def chat_csv(df, question):
    context = df.to_dict('list')
    context = f"""You are a senior data scientist. Below is a dataset where the dataframe has been converted into a dictionary. The keys represent the column names, and the values correspond to the data in each column. Please analyze the data and answer the question based on the provided context. If the context is insufficient or irrelevant, indicate that there is not enough information available. Do not use external knowledge beyond what is presented in the dataset.
    Don't showw how you did it, give the final answer.
            {context}
    """

    prompt = f"Question: {question}"
    response = client.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=[
        {"role": "system", "content": context},
        {"role": "user", "content": prompt}
    ]
    )

    response = response.choices[0].message
    response = response.content
    return response

df  = pd.read_csv("NIMC.csv")
question = "Give me a summary about the population and list the top three states with the highest population."
answer = chat_csv(df, question)
print(answer)
