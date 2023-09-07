# chatbot_app/views.py
from django.shortcuts import render
import openai
import pandas as pd
import numpy as np
import faiss

openai.api_key = "GHHJHJHKJLKJLJL"

# Load and concatenate your vectorized datasets
df1 = pd.read_csv(r'C:\Users\shuri\SAMSGPT\Databases\datalink1.csv')
df2 = pd.read_csv(r'C:\Users\shuri\SAMSGPT\Databases\datalink2.csv')
df3 = pd.read_csv(r'C:\Users\shuri\SAMSGPT\Databases\datalink3.csv')

all_vectorized_data = pd.concat([df1, df2, df3], ignore_index=True).values

# chatbot_app/views.py
def chatbot(request):
    if request.method == 'POST':
        user_input = request.POST.get('message')
        if user_input:
            # Perform vector search using FAISS
            query_vector = np.array([user_input], dtype=np.float32)
            index = faiss.IndexFlatIP(all_vectorized_data.shape[1])
            index.add(all_vectorized_data)
            _, search_results = index.search(query_vector, k=5)

            # Get the relevant historical data points
            relevant_data = [all_vectorized_data[idx] for idx in search_results[0]]

            # Create a prompt using the user input and relevant historical data
            historical_messages = '\n'.join(relevant_data)
            prompt = f"You: {user_input}\nRelevant History: {historical_messages}\nBot:"

            # Generate a response using OpenAI's GPT model
            response = openai.Completion.create(
                engine="davinci",  # Choose the appropriate engine
                prompt=prompt,
                max_tokens=50
            )
            bot_response = response.choices[0].text.strip()
            return render(request, 'chatbot.html', {'user_input': user_input, 'bot_response': bot_response})

    return render(request, 'chatbot.html')
