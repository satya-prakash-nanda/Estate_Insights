import streamlit as st
import pickle
import pandas as pd
import numpy as np
# import joblib

st.set_page_config(page_title="Viz Demo")

# load dataframe
with open('df.pkl', 'rb') as file:
    df = pickle.load(file)

# load pipeline
try:
    with open('pipeline.pkl', 'rb') as file:
        pipeline = pickle.load(file)
except Exception as e:
    st.error(f"An error occurred while loading the pipeline: {e}")


# st.dataframe(df)

st.header('Enter your inputs')

# property_type
property_type = st.selectbox('Property Type', ['flat', 'house'])

# sector
sector = st.selectbox('sector', sorted(df['sector'].unique().tolist()))

# bedroom
bedroom = float(st.selectbox('Number of bedrooms', sorted(df['bedRoom'].unique().tolist())))

# bathroom
bathroom = float(st.selectbox('Number of bathrooms', sorted(df['bathroom'].unique().tolist())))

# balcony
balcony = st.selectbox('Number of balcony', sorted(df['balcony'].unique().tolist()))

# agePossession       object
property_age = st.selectbox('Property Age', sorted(df['agePossession'].unique().tolist()))

# built_up_area      float64
built_up_area = float(st.number_input('Built Up Area'))

# servant room       float64
servant_room = float(st.selectbox('Servant Room', [0.0, 1.0]))

# store room         float64
store_room = float(st.selectbox('Store Room', [0.0, 1.0]))

# furnishing_type     object
furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique().tolist()))

# luxury_category     object
luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique().tolist()))

# floor_category      object
floor_category = st.selectbox('Floor Category', sorted(df['floor_category'].unique().tolist()))


if st.button('Predict'):
    # form a dataframe
    data = [[property_type, sector, bedroom, bathroom, balcony, property_age, built_up_area, servant_room, store_room,
             furnishing_type, luxury_category, floor_category]]
    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony', 'agePossession', 'built_up_area',
               'servant room', 'store room', 'furnishing_type', 'luxury_category', 'floor_category']

    # predict
    one_df = pd.DataFrame(data, columns=columns)
    # st.dataframe(one_df)

    try:
        base_price = np.expm1(pipeline.predict(one_df))[0]
        low = base_price - 0.22
        high = base_price + 0.22
        st.text(f"The estimated price of the property is between ₹{round(low, 2)}Cr and ₹{round(high, 2)}Cr.")
    except Exception as e:
        st.error(f"Prediction failed: {e}")
