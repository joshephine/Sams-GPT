import pandas as pd

# Load LinkedIn messages data
messages_df = pd.read_csv(r'C:\Users\shuri\OneDrive\Desktop\messages.csv')

# Load LinkedIn connections data
connections_df = pd.read_csv(r'C:\Users\shuri\OneDrive\Desktop\connections.csv')

# Load LinkedIn invitations data
invitations_df = pd.read_csv(r'C:\Users\shuri\OneDrive\Desktop\invitations.csv')

# Print the first few rows of each DataFrame to verify the data loading
print("LinkedIn Messages Data:")
print(messages_df.head())

print("\nLinkedIn Connections Data:")
print(connections_df.head())

print("\nLinkedIn Invitations Data:")
print(invitations_df.head())






