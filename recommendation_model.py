import openai
import pandas as pd
from surprise import Dataset, Reader, KNNBasic
import spacy
import os

# Set up spaCy for NLP
nlp = spacy.load("en_core_web_sm")

# Set your OpenAI API key
openai.api_key = "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"

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('user_responses.csv')

# Convert 'Intensity' column to numeric values
intensity_mapping = {'Very Weak': 1, 'Weak': 2, 'Moderate': 3, 'Strong': 4, 'Very Strong': 5}
df['Intensity'] = df['Intensity'].map(intensity_mapping)

# Load your dataset from the pandas DataFrame
reader = Reader(line_format='user item rating', rating_scale=(1, 5))
data = Dataset.load_from_df(df[['user', 'Notes', 'Intensity']], reader)

# Use the KNNBasic collaborative filtering algorithm
sim_options = {'name': 'cosine', 'user_based': False}
model = KNNBasic(sim_options=sim_options)

# Train the model on the entire dataset
trainset = data.build_full_trainset()
model.fit(trainset)

# Read the perfume data into a separate DataFrame
perfume_df = pd.read_csv('final_perfume_data.csv')

# Function to extract entities from user input using spaCy
def extract_entities(user_input):
    doc = nlp(user_input)
    entities = [ent.text for ent in doc.ents]
    return entities

# Function to get a scent recommendation from GPT-3
def get_gpt3_recommendation(user_id, scent_name):
    prompt = f"User {user_id} likes the scent {scent_name}. Suggest a similar scent."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Assuming you want to recommend perfumes based on the extracted entities
def process_user_responses(user_responses):
    user_id = user_responses[0]  # Assuming the first response is the user ID
    scent_name = user_responses[-1]  # Assuming the last response is the scent name

    # Process user input using NLP
    entities = extract_entities(scent_name)
    print(f"Extracted entities: {entities}")

    # Predict rating using collaborative filtering
    prediction = model.predict(user_id, scent_name)
    predicted_rating = prediction.est
    print(f"Predicted rating for user {user_id} and scent {scent_name}: {predicted_rating}")

    # Get a scent recommendation from GPT-3
    gpt3_recommendation = get_gpt3_recommendation(user_id, scent_name)
    print(f"GPT-3 recommendation based on user's liking: {gpt3_recommendation}")

    # Get perfume recommendations based on user responses
    perfume_recommendations = perfume_df[perfume_df['Notes'].isin(entities)]
    print("\nPerfume Recommendations:")
    print(perfume_recommendations[['Name', 'Brand', 'Notes']])

    return {
        'gpt3_recommendation': gpt3_recommendation,
        'perfume_recommendations': perfume_recommendations.to_dict(orient='records')
    }

if __name__ == "__main__":
    # Example usage of the recommendation model
    user_responses = ['user1', 'floral', '4']
    result = process_user_responses(user_responses)
    print(result)
