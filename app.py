import streamlit as st
import pandas as pd
import pickle

# Load the cleaned dataset
data = pd.read_csv('used_cars.csv')
data['milage'] = data['milage'].str.replace(',', '').str.replace(' mi.', '').astype(float)
data['price'] = data['price'].str.replace(',', '').str.replace('$', '').astype(float)
data = data.dropna(subset=['brand', 'model', 'model_year', 'price'])

# Load the pre-trained model
with open('car_price_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Streamlit app
st.title("Prediksi Harga Mobil")

# User inputs
brand = st.selectbox("Select Brand:", options=data['brand'].unique())
filtered_models = data[data['brand'] == brand]['model'].unique()
model_input = st.selectbox("Select Model:", options=filtered_models)
model_year = st.number_input("Enter Model Year:", min_value=1980, max_value=2025, step=1, value=2020)
milage = st.number_input("Enter Mileage (in miles):", min_value=0, step=5000, value=50000)

# Prediction button
if st.button("Predict Price"):
    # Make a prediction
    input_data = pd.DataFrame({
        'brand': [brand],
        'model': [model_input],
        'model_year': [model_year],
        'milage': [milage]
    })
    predicted_price = model.predict(input_data)[0]
    st.success(f"Estimated Price: ${predicted_price:,.2f}")

# Note: Model training is skipped during app runtime to enhance performance.
