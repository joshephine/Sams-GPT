import pandas as pd
import mysql.connector
from mysql.connector import Error
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import re

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Load your LinkedIn data (messages, connections, invitations) as pandas DataFrames


# Messages
messages_df = pd.read_csv(r'C:\Users\shuri\OneDrive\Desktop\messages.csv')

# Connections
connections_df = pd.read_csv(r'C:\Users\shuri\OneDrive\Desktop\connections.csv')

# Invitations
invitations_df = pd.read_csv(r'C:\Users\shuri\OneDrive\Desktop\invitations.csv')

# Clean and preprocess text data
def preprocess_text(text):
    if isinstance(text, str):
        text = re.sub(r'http\S+', '', text)  # Remove URLs
        text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove non-alphabet characters
        text = text.lower()  # Convert to lowercase
        return text
    else:
        return ''  # Return empty string for non-string values


# Database connection
try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",  # Change to your MySQL username
        password="GHHHJH",  # Change to your MySQL password
        database="mychat"  # Change to your MySQL database name
    )

    if connection.is_connected():
        cursor = connection.cursor()

        # Create tables if they don't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS linkedin_messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sender VARCHAR(255),
                receiver VARCHAR(255),
                content MEDIUMTEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS linkedin_connections (
                id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(255),
                last_name VARCHAR(255),
                company VARCHAR(255),
                position VARCHAR(255)
                       
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS linkedin_invitations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sender VARCHAR(255),
                receiver VARCHAR(255)
            )
        """)

        # Store LinkedIn messages
        for index, row in messages_df.iterrows():
            cleaned_text = preprocess_text(row['CONTENT'])[:255]  # Limit content to 255 characters
            query = "INSERT INTO linkedin_messages (sender, receiver, content) VALUES (%s, %s, %s)"
            values = (row['FROM'], row['TO'], cleaned_text)
            cursor.execute(query, values)
        

        # Store LinkedIn connections
        for index, row in connections_df.iterrows():
            query = "INSERT INTO linkedin_connections (first_name, last_name,company,position) VALUES (%s, %s, %s,%s)"
            values = (row['First Name'], row['Last Name'], row['company'],row['position'])
            cursor.execute(query, values)
        

        # Store LinkedIn invitations
        for index, row in invitations_df.iterrows():
            query = f"INSERT INTO linkedin_invitations (sender, receiver) VALUES ('{row['From']}', '{row['To']}')"
            cursor.execute(query)

        connection.commit()
        print("Data pushed successfully!")

except Error as e:
    print("Error:", e)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
