import streamlit as st
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt





# Set page config to use the full width
st.set_page_config(layout="wide")
st.title(" Food Price Changes In Sri Lanka Over the Time")
#import dataset
df = pd.read_csv("SL_FoodPriceChanges.csv")
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
    District = df['District'].dropna().unique()
    selected_district = st.sidebar.selectbox("Choose a district", sorted(District))
    # Filter data based on selection
    filtered_df = df[df['District'] == selected_district]
     # ✅ Apply ALL filters at once
    filtered_df = df[
        (df['category'] == selected_category) &
        (df['commodity'] == selected_commodity) &
        (df['pricetype'] == selected_saletype) &
        (df['District'] == selected_district) 
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
    # Title for the Streamlit page
    st.title("Categories by Economic Centers")

    # Filter dataset
    economic_centers = [
        'Economic Centre-Dambulla', 
        'Economic Centre - Peliyagoda', 
        'Economic Centre-Pettah', 
        'Fish market-Peliyagoda', 
        'Fish market-Negombo', 
        'Economic Centre-Maradagahamula',
        'National Average'
    ]


    filtered_df = df[df['market'].isin(economic_centers)]
    
   
    category_options = filtered_df['category'].unique()
    selected_category = st.selectbox("Select Category", category_options)
    # Filter by selected category
    category_df = filtered_df[filtered_df['category'] == selected_category]

    # Group by market and calculate average price
    price_comparison = category_df.groupby('market')['price'].mean()

    # Extract national average
    national_avg = price_comparison.get('National Average', None)

    # Remove national average from other centers
    market_prices = price_comparison.drop('National Average', errors='ignore')
    plot_df = pd.DataFrame({
        'Economic Center Price': market_prices,
        'National Average': national_avg
    })
    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    plot_df.plot(kind='bar', ax=ax)

    ax.set_title(f"{selected_category} – Economic Centers vs National Average")
    ax.set_xlabel("Economic Center")
    ax.set_ylabel("Average Price")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Show plot
    st.pyplot(fig)
    
    
if page == "Overview":

    st.markdown(
        "<p style='font-size:22px; color:White;'>Overview:</p>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='font-size:18px; color:orange;'>Here's the first few rows of dataset (After Preparation):</p>",
        unsafe_allow_html=True
    )
    # Display the DataFrame
    st.dataframe(df.head())
    st.markdown(
        """
        <br>
        <p style='font-size:18px; color:orange;'>🔧 Data Preparation Steps:</p>
        <ul style='font-size:16px; color:white;'>
            <li>🧹 Imputed missing values in key columns to ensure data completeness.</li>
            <li>📅 Converted column data types (e.g., date fields to datetime).</li>
            <li>🗑️ Removed irrelevant rows and outlier records based on domain knowledge.</li>
            <li>✏️ Renamed columns for clarity and consistency.</li>
            <li>🧪 Filtered dataset to include only selected economic centers and relevant categories.</li>
            <li>🔍 Ensured consistency in category and market names for easier filtering and analysis.</li>
        </ul>
        """,
        unsafe_allow_html=True
    )

    # Create three columns
    col1, col2, col3 = st.columns(3)

    # ---- Column 1: Summary Statistics ----
    with col1:
        st.markdown(
        "<p style='font-size:18px; color:orange;'>📊 Summary Statistics</p>",
        unsafe_allow_html=True
        )

         
    
        st.dataframe(df.describe())
    # ---- Column 2: DataFrame Info ----
    with col2:
        st.markdown(
        "<p style='font-size:18px; color:orange;'>🧾 Dataset Info</p>",
        unsafe_allow_html=True
        )
    

        # Use df.dtypes and df.isnull().sum() to create a table manually
        info_table = pd.DataFrame({
            'Column': df.columns,
            'Non-Null Count': df.notnull().sum().values,
            'Dtype': df.dtypes.values
        })

        # Reset index for clean display
        info_table.reset_index(drop=True, inplace=True)

        # Display as a table
        st.dataframe(info_table)

    # ---- Column 3: Missing Values Count ----
    with col3:
        st.markdown(
        "<p style='font-size:18px; color:orange;'>❗ Missing Values</p>",
        unsafe_allow_html=True
        )
    
        missing_counts = df.isnull().sum()
        missing_df = missing_counts[missing_counts > 0].reset_index()
        missing_df.columns = ['Column', 'Missing Values']
    
        if not missing_df.empty:
            st.dataframe(missing_df)
        else:
            st.success("No missing values found 🎉")
    


            





