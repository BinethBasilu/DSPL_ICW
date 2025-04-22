import streamlit as st
import pandas as pd
import numpy as np
import datetime



# Set page config to use the full width
st.set_page_config(layout="wide")
st.title(" Food Price Changes In Sri Lanka Over the Time")
#import dataset
df = pd.read_csv("SL_FoodPrice.csv")
df['date'] = pd.to_datetime(df['date'], errors='coerce')
st.write("Here's the dataset:")
st.dataframe(df)
# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Food Prices", "Overview", "About"])
# Backgrounds
backgrounds = {
    "Food Prices": "https://t4.ftcdn.net/jpg/10/58/65/25/240_F_1058652594_bg5k6yBDcEtfZ6T9icIcfihMBliATUtu.jpg",
    "Overview": "https://t3.ftcdn.net/jpg/11/82/77/14/240_F_1182771481_jlr0QvZbcuPbZxV7CEhpH43BqNftUU7o.jpg",
    "About": "https://t4.ftcdn.net/jpg/10/58/65/21/240_F_1058652183_nPq8AkiuSfMZbZ92UqISAyypSZ57Pi0c.jpg"
}
# Function to set background
def set_background(image_url):
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.4); /* fading dark overlay */
            z-index: 0;
        }}
        </style>
    """, unsafe_allow_html=True)

set_background(backgrounds[page])
if page == "Food Prices":
    st.sidebar.subheader('Query Parameter')
    start_date = st.sidebar.date_input("Start date", datetime.date(2004, 1, 15))
    end_date = st.sidebar.date_input("End date", datetime.date(2025, 3, 15))

    st.sidebar.header("Filter by food category")

    # Get unique food categories
    categories = df['category'].dropna().unique()
    selected_category = st.sidebar.selectbox("Choose a food category", sorted(categories))

    # Filter data to get commodities only under the selected category
    filtered_commodities = df[df['category'] == selected_category]['commodity'].dropna().unique()

    # Select food name from only the filtered commodities
    selected_commodity = st.sidebar.selectbox("Choose a food name", sorted(filtered_commodities))

    # Final filter: based on selected food name
    filtered_df = df[(df['category'] == selected_category) & (df['commodity'] == selected_commodity)]
    # Get unique categories from the 'category' column
    sale_Type = df['pricetype'].dropna().unique()
    selected_saletype = st.sidebar.selectbox("Choose a price type", sorted(sale_Type))
    # Filter data based on selection
    filtered_df = df[df['pricetype'] == selected_saletype]
    # Get unique categories from the 'category' column
    District = df['district'].dropna().unique()
    selected_district = st.sidebar.selectbox("Choose a district", sorted(District))
    # Filter data based on selection
    filtered_df = df[df['district'] == selected_district]
     # ✅ Apply ALL filters at once
    filtered_df = df[
        (df['category'] == selected_category) &
        (df['commodity'] == selected_commodity) &
        (df['pricetype'] == selected_saletype) &
        (df['district'] == selected_district) 
    ]
    filtered_df = filtered_df[
        filtered_df['date'].between(pd.to_datetime(start_date), pd.to_datetime(end_date))
    ]
    # Show table
    st.write(f"### Prices for {selected_commodity} ({selected_saletype}) in {selected_category}")
    st.dataframe(filtered_df)

    # Line Chart: Price Trend
    st.markdown(
    "<h3 style='color: orange;'>📈 Price Trend Over Time</h3>", 
    unsafe_allow_html=True
)

    if 'date' in filtered_df.columns and 'price' in filtered_df.columns and not filtered_df.empty:
        price_chart_data = filtered_df.groupby('date')['price'].mean().reset_index()
        st.line_chart(price_chart_data, x='date', y='price')
    else:
        st.warning("Filtered data is empty or missing 'SL_FoodPrice'/'price' columns.")

if page == "Overview":
    



