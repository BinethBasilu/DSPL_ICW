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
st.sidebar.title("Content")
page = st.sidebar.selectbox("Choose a page", ["Food Prices", "Overview", "About"])
# Backgrounds
backgrounds = {
    "Food Prices": "https://t4.ftcdn.net/jpg/10/58/65/25/240_F_1058652594_bg5k6yBDcEtfZ6T9icIcfihMBliATUtu.jpg",
    "Overview": "https://t3.ftcdn.net/jpg/11/82/77/14/240_F_1182771481_jlr0QvZbcuPbZxV7CEhpH43BqNftUU7o.jpg",
    "About": "data:image/jpeg;base64,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"
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
    st.sidebar.header("Filter by food category")

    # Get unique food categories
    categories = df['category'].dropna().unique()
    selected_category = st.sidebar.selectbox("Choose a food category", sorted(categories))

    # Filter data to get commodities only under the selected category
    filtered_commodities = df[df['category'] == selected_category]['commodity'].dropna().unique()

    # Select food name from only the filtered commodities
    selected_commodity = st.sidebar.selectbox("Choose foods", sorted(filtered_commodities))

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
    # --- Title ---
    st.title("📈 Price Changes Over Time")

    # --- Sidebar Filters ---
    st.sidebar.header("Filter Options")

    # Date range filter
    start_date = st.sidebar.date_input("Start Date", datetime.date(2004, 1, 15))
    end_date = st.sidebar.date_input("End Date", datetime.date(2025, 3, 15))

    # Category selection
    categories = df['category'].dropna().unique()
    selected_category = st.sidebar.selectbox("Select Food Category", sorted(categories))

    # Commodity (food item) multiselect based on selected category
    filtered_commodities = df[df['category'] == selected_category]['commodity'].dropna().unique()
    selected_commodities = st.sidebar.multiselect("Select Food Items", sorted(filtered_commodities))

    # Price type filter
    sale_types = df['pricetype'].dropna().unique()
    selected_saletype = st.sidebar.selectbox("Select Price Type", sorted(sale_types))

    # Filter dataset
    filtered_df = df[
        (df['category'] == selected_category) &
        (df['commodity'].isin(selected_commodities)) &
        (df['pricetype'] == selected_saletype) &
        (df['date'] >= pd.to_datetime(start_date)) &
        (df['date'] <= pd.to_datetime(end_date))
    ]


    # --- Plot ---
    if not selected_commodities:
        st.warning("Please select at least one food item to view the price trend.")
    elif filtered_df.empty:
        st.info("No data available for the selected filters.")
    else:
        st.subheader(f"📊 Price Trends for {selected_category} ({selected_saletype})")

        # Plot line chart using matplotlib
        fig, ax = plt.subplots(figsize=(12, 6))
        for commodity in selected_commodities:
            data = filtered_df[filtered_df['commodity'] == commodity]
            ax.plot(data['date'], data['price'], label=commodity)

        ax.set_title(f"Price Changes Over Time – {selected_category}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price (LKR)")
        ax.legend(title="Food Item")
        ax.grid(True)
        plt.tight_layout()

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
        # Styled heading
        st.markdown(
            "<p style='font-size:18px; color:orange; font-weight:bold;'>❗ Missing Values</p>",
            unsafe_allow_html=True
        )

        # Calculate missing values
        missing_counts = df.isnull().sum()
        missing_df = missing_counts[missing_counts > 0].reset_index()
        missing_df.columns = ['Column', 'Missing Values']

        if not missing_df.empty:
            # Show as DataFrame
            st.dataframe(missing_df)
        else:
            # Styled success message
            st.markdown(
                """
                <div style='
                    background-color:#e6f4ea;
                    color:#207a43;
                    padding:15px;
                    border-left: 5px solid #2ecc71;
                    border-radius: 8px;
                    font-size:16px;
                    '>
                    No missing values found 🎉
                </div>
                """,
                unsafe_allow_html=True
            )
        

if page == "About":
    import os

    # --- Page Title ---
    st.title("📚 About Food Categories")

    # Load dataset (replace with your actual DataFrame if needed)
    # df = pd.read_csv("your_data.csv")

    # Get unique categories
    categories = df['category'].dropna().unique()

    # Select food category
    selected_category = st.selectbox("Select a Food Category", sorted(categories))

    # Category descriptions (add more as needed)
    category_descriptions = {
        "cereals and tubers": "Cereals like rice, wheat, and maize, along with tubers such as potatoes, yams, and cassava, form the backbone of diets across the world. They are primary sources of complex carbohydrates, providing energy, dietary fiber, and essential nutrients. These staples are not just filling—they're foundational to food security and cultural cuisines.",
        "meat, fish and eggs": "This category delivers high-quality proteins crucial for muscle development, hormone production, and immune function. Meat and fish offer important nutrients like iron, zinc, and omega-3 fatty acids, while eggs are a powerhouse of vitamins and healthy fats. Together, they form a cornerstone of many balanced diets.",
        "miscellaneous food": "This diverse category includes a mix of food items that don't strictly belong to the main groups—ranging from processed foods, snacks, and condiments to specialty ingredients. Though varied, these foods often enhance flavor, convenience, and cultural diversity in diets when consumed in moderation.",
        "oil and fats": "Oils and fats—whether from plants like coconut and sunflower or animal sources like ghee and butter—play a vital role in flavor, texture, and nutrition. They provide essential fatty acids, aid in the absorption of fat-soluble vitamins (A, D, E, K), and serve as a dense source of energy. Used wisely, they support both culinary richness and health.",
        "pulses and nuts": "A powerhouse of plant-based nutrition, pulses (like lentils, beans, and chickpeas) and nuts (like cashews and almonds) are rich in protein, fiber, and heart-healthy fats. They contribute to sustainable diets and are a vital source of nutrients for vegetarians and vegans.",
        "vegetables and fruits": "Colorful, vibrant, and nutrient-dense—fruits and vegetables are the champions of health. They are loaded with essential vitamins, minerals, antioxidants, and fiber that help prevent disease, support digestion, and boost immunity. A diverse intake is key to overall well-being and vitality."
    }


    # Category image path (image per category)
    category_images = {
        "cereals and tubers": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSGoG0zWA2Swi132IwbXh9if8EoaR1bgYHEuw&s",
        "meat, fish and eggs": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRYLm0THhvanao7aWofOQzflpos3T_W2VEvyQ&s",
        "miscellaneous food": "https://thumbs.dreamstime.com/b/close-up-chopped-hot-chili-peppers-heaps-salt-sugar-garlic-allspice-bay-leaf-old-wooden-surface-selective-close-up-156240684.jpg",
        "oil and fats": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQBK51naBmSGfzjapHrjdDI7W6QP6WbHUkELg&s",
        "pulses and nuts": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQYgOa8tQlXNO7l37zGMF7I-dKWd96SmX2H-Q&s",
        "vegetables and fruits": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQOGpxLJbhDOSQ8HoXlJmUnvt8PTSN5HKApRw&s"
    }


    # --- Display Image + Description ---
    styled_description = f"""
    <div style='font-size:18px; color:#2c3e50; background-color:#f0f8ff; padding: 15px; border-radius: 10px;'>
       {category_descriptions.get(selected_category, "No description available.")}
    </div>
    """
    st.markdown(styled_description, unsafe_allow_html=True)

    st.image(category_images.get(selected_category, ""), caption=selected_category, width=350)
    

    # --- Show all food items in that category ---
    st.markdown(f"### 🧺 Food Items in {selected_category}:")
    food_items = df[df['category'] == selected_category]['commodity'].dropna().unique()
    styled_food_items = f"""
    <div style='font-size:17px; color:#1e3d59; background-color:#f9f9f9; padding: 15px; border-left: 5px solid #ff914d; border-radius: 8px;'>
        {", ".join(sorted(food_items))}
    </div>
    """
    st.markdown(styled_food_items, unsafe_allow_html=True)
            
    


            





