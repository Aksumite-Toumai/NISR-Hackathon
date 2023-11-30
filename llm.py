import os
from dotenv import load_dotenv  # type: ignore
from openai import OpenAI  # type: ignore

# Load environment variables
load_dotenv()

# Retrieve OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)


def chat_with_csv(df, chart_type):
    context = df.to_dict('list')
    context = f"""You are a senior data scientist. Below is a dataset where the dataframe has been converted into a dictionary.
    The keys represent the column names, and the values correspond to the data in each column.
    We have used this dataset to plot a {chart_type} line.
    Please analyze the data and answer the question based on the provided context. If the context is insufficient or irrelevant,
    indicate that there is not enough information available.
    Do not use external knowledge beyond what is presented in the dataset.
    Don't showw how you did it, give the final answer.
    The dataset is from Rwanda and the currency is RWF.
            {context}
    """

    prompt = "Explain the chart"
    try:
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
    except Exception:  # type: ignore
        return "Something goes wrong.try it again later!"
# df = pd.read_csv("NIMC.csv")
# query = input("Enter your query: ")
# result = chat_with_csv(df, query)
# print(result)
