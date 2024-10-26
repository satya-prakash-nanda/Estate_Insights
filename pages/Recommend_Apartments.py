import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title="Recommendation")

# Load data
location_df = pickle.load(open('location_distance.pkl', 'rb'))
cosine_sim1 = pickle.load(open('cosine_sim1.pkl', 'rb'))
cosine_sim2 = pickle.load(open('cosine_sim2.pkl', 'rb'))
cosine_sim3 = pickle.load(open('cosine_sim3.pkl', 'rb'))

st.title('Select Location and Radius')

# Location and Radius input
Location = st.selectbox('Location', sorted(location_df.columns.to_list()))
Radius = st.number_input('Radius in Kms')

# Search button for nearby properties
if st.button('Search'):
    result = location_df[location_df[Location] < Radius * 1000][Location].sort_values()

    if result.empty:
        # Display a clear message when no apartments are found
        st.warning(f"No apartments found within {Radius} Kms of {Location}.")
        st.info("Try expanding your search radius or selecting a different location.")
    else:
        for key, value in result.items():
            st.text(f"{key} - {round(value / 1000)} Kms")


st.title('Recommend Apartments')
# Sliders for user-defined weights
n1 = st.slider("Weight for Facilities Similarity", 0, 100, 30)
n2 = st.slider("Weight for BHK and Price Similarity", 0, 100, 20)
n3 = st.slider("Weight for Location Similarity", 0, 100, 8)

# Function to recommend properties based on similarity scores
def recommend_properties_with_scores(property_name, top_n=10):
    cosine_sim_matrix = n1 * cosine_sim1 + n2 * cosine_sim2 + n3 * cosine_sim3

    # Debug: Print property_name
    print(f"Property name selected: {property_name}")

    try:
        # Get the similarity scores for the property using its name as the index
        sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))
    except KeyError:
        st.error(f"Property name '{property_name}' not found in the index.")
        return None  # Early return on error

    # Sort properties based on the similarity scores
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices of the top_n most similar properties
    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]

    # Retrieve the names of the top properties using the indices
    top_properties = location_df.index[top_indices].tolist()

    return top_properties

# Streamlit UI for recommendations

selected_apartment = st.selectbox('Select an Apartment', sorted(location_df.index.to_list()))

if st.button('Recommend'):
    recommended_properties = recommend_properties_with_scores(selected_apartment)

    if recommended_properties is not None:
        for property_name in recommended_properties:
            st.text(property_name)

