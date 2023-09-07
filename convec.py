import pandas as pd
import mysql.connector
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')

# Database connection
try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",  # Change to your MySQL username
        password="7687UGUGUI",  # Change to your MySQL password
        database="mychat"  # Change to your database name
    )

    if connection.is_connected():
        cursor = connection.cursor()

        # Load data from the linkedin_messages table
        messages_query = "SELECT * FROM linkedin_messages"
        cursor.execute(messages_query)
        messages_data = cursor.fetchall()

        # Create a DataFrame from the data
        messages_df = pd.DataFrame(messages_data, columns=["id", "sender", "receiver", "content"])

        # Handle missing values by replacing NaN with an empty string
        messages_df["content"] = messages_df["content"].fillna("")

        # Tokenize the text for Word2Vec training
        messages_text_tokens = [word_tokenize(text) for text in messages_df['content']]

        # Train Word2Vec model
        word2vec_model = Word2Vec(sentences=messages_text_tokens, vector_size=100, window=5, min_count=1, sg=0)

        # Initialize an empty list to store the embeddings
        embeddings = []

        # Iterate through the DataFrame and calculate embeddings
        for i, row in messages_df.iterrows():
            text_tokens = word_tokenize(row['content'])
            # Check if there are any tokens to calculate embeddings for
            if text_tokens:
                vector = word2vec_model.wv[text_tokens].mean(axis=0)
                embeddings.append(vector)
            else:
                # If no tokens, add a vector of zeros
                embeddings.append([0] * 100)  # Change 100 to your vector size

        # Create a DataFrame from the embeddings
        embeddings_df = pd.DataFrame(embeddings, columns=[f"embedding_{i}" for i in range(100)])  # Change 100 to your vector size

        print("Embeddings shape:", embeddings_df.shape)

         # Load data from the linkedin_connections table
        connections_query = "SELECT * FROM linkedin_connections"
        cursor.execute(connections_query)
        connections_data = cursor.fetchall()

        # Create a DataFrame from the data
        connections_df = pd.DataFrame(connections_data, columns=["id", "first_name", "last_name", "company", "position"])

        # Handle missing values by replacing NaN with an empty string
        connections_df["company"] = connections_df["company"].fillna("")
        connections_df["position"] = connections_df["position"].fillna("")

        # Combine relevant columns into a single text column
        connections_df["text"] = connections_df["first_name"] + " " + connections_df["last_name"] + " " + connections_df["company"] + " " + connections_df["position"]

        # Convert the text column to string
        connections_df["text"] = connections_df["text"].astype(str)

        # Tokenize the text for Word2Vec training
        connections_text_tokens = [word_tokenize(text) for text in connections_df['text']]

        # Train Word2Vec model
        word2vec_model = Word2Vec(sentences=connections_text_tokens, vector_size=100, window=5, min_count=1, sg=0)

        # Initialize an empty list to store the embeddings
        embeddings1 = []

        # Iterate through the DataFrame and calculate embeddings
        for i, row in connections_df.iterrows():
            text_tokens = word_tokenize(row['text'])
            # Check if there are any tokens to calculate embeddings for
            if text_tokens:
                vector = word2vec_model.wv[text_tokens].mean(axis=0)
                embeddings1.append(vector)
            else:
                # If no tokens, add a vector of zeros
                embeddings1.append([0] * 100)  # Change 100 to your vector size

        # Create a DataFrame from the embeddings
        embeddings_df1 = pd.DataFrame(embeddings1, columns=[f"embedding_{i}" for i in range(100)])  # Change 100 to your vector size

        print("Embeddings shape for connections:", embeddings_df1.shape)

         # Load data from the linkedin_invitations table
        invitations_query = "SELECT * FROM linkedin_invitations"
        cursor.execute(invitations_query)
        invitations_data = cursor.fetchall()

        # Create a DataFrame from the data
        invitations_df = pd.DataFrame(invitations_data, columns=["id", "sender", "receiver"])

        # Combine sender and receiver columns into a single text column
        invitations_df["text"] = invitations_df["sender"] + " " + invitations_df["receiver"]

        # Remove any NaN or missing values
        invitations_df.dropna(subset=["text"], inplace=True)

        # Convert the text column to string
        invitations_df["text"] = invitations_df["text"].astype(str)

        # Tokenize the text for Word2Vec training
        invitations_text_tokens = [word_tokenize(text) for text in invitations_df['text']]

        # Train Word2Vec model
        word2vec_model = Word2Vec(sentences=invitations_text_tokens, vector_size=100, window=5, min_count=1, sg=0)

        # Initialize an empty list to store the embeddings
        embeddings2 = []

        # Iterate through the DataFrame and calculate embeddings
        for text_tokens in invitations_text_tokens:
            # Check if there are any tokens to calculate embeddings for
            if text_tokens:
                vector = word2vec_model.wv[text_tokens].mean(axis=0)
                embeddings2.append(vector)
            else:
                # If no tokens, add a vector of zeros
                embeddings2.append([0] * 100)  # Change 100 to your vector size

        # Create a DataFrame from the embeddings
        embeddings_df2 = pd.DataFrame(embeddings2, columns=[f"embedding_{i}" for i in range(100)])  # Change 100 to your vector size

        print("Embeddings shape for invitations:", embeddings_df2.shape)

        embeddings_df.to_csv("datalink1.csv", index=False)
        embeddings_df1.to_csv("datalink2.csv", index=False)
        embeddings_df2.to_csv("datalink3.csv", index=False)




except Exception as e:
    print("Error:", e)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
