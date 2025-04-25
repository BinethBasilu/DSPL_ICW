import streamlit as st
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import plotly.express as px

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
    "<h3 style='color: orange;'> Price Trend Over Time</h3>", 
    unsafe_allow_html=True
    )


    if 'date' in filtered_df.columns and 'price' in filtered_df.columns and not filtered_df.empty:
        price_chart_data = filtered_df.groupby('date')['price'].mean().reset_index()
        st.line_chart(price_chart_data, x='date', y='price')
    else:
        st.warning("Filtered data is empty or missing 'SL_FoodPrice'/'price' columns.")
    # Page title
    st.title("Economic Centers vs National Average")

    # Economic centers list (including national average)
    economic_centers = [
        'Economic Centre-Dambulla', 
        'Economic Centre - Peliyagoda', 
        'Economic Centre-Pettah', 
        'Fish market-Peliyagoda', 
        'Fish market-Negombo', 
        'Economic Centre-Maradagahamula',
        'National Average'
    ]


    # Filter to include only relevant markets
    filtered_df = df[df['market'].isin(economic_centers)]

    # Select category from dropdown
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

    bar_df = (
    market_prices.reset_index(name='Economic Center Price')
    .rename(columns={'market': 'Economic Center'})
    )


    # add a column that repeats the national average for each center
    bar_df['National Average'] = national_avg

    # reshape to “long” format → Economic Center, Series, Average Price
    bar_df = bar_df.melt(
        id_vars='Economic Center',
        var_name='Series',
        value_name='Average Price'
    )


    # ─── Plot ──────────────────────────────────────────────────────
    fig_bar = px.bar(
        bar_df,
        x='Economic Center',
        y='Average Price',
        color='Series',
        barmode='group',                 # side‑by‑side bars; use 'stack' if you prefer
        title=f"{selected_category} – Economic Centers vs National Average",
        height=550
    )
    fig_bar.update_layout(
        xaxis_title='Economic Center',
        yaxis_title='Average Price (LKR)',
        legend_title_text='',
        margin=dict(l=30, r=30, t=60, b=40)
    )

    st.plotly_chart(fig_bar, use_container_width=True)
    # Assuming you've already read and processed your dataset
    df['year_month'] = df['date'].dt.to_period('M').astype(str)

    # Sidebar: Select month-year
    available_months = sorted(df['year_month'].dropna().unique())
    selected_month = st.sidebar.selectbox("Select a Year-Month", available_months)

    # Filter data for selected year-month
    df_month = df[df['year_month'] == selected_month]
    # Dropdown to select year and month
    selected_period = st.selectbox("Select Year and Month", sorted(df['year_month'].unique()))

    # Filter data by selected year and month
    df_month = df[df['year_month'] == selected_period]

    # National Averages
    national_avg = (
        df_month[df_month['market'] == "National Average"]
        .groupby('commodity')['price']
        .mean()
        .reset_index()
        .rename(columns={'price': 'National Average Price'})
    )

    # Highest Prices
    max_prices = df_month.loc[df_month.groupby('commodity')['price'].idxmax()]
    max_df = max_prices[['commodity', 'market', 'price']].rename(columns={
        'market': 'Market (Highest)',
        'price': 'Highest Price'
    })


    max_df = pd.merge(max_df, national_avg, on='commodity', how='left')

    # Lowest Prices
    min_prices = df_month.loc[df_month.groupby('commodity')['price'].idxmin()]
    min_df = min_prices[['commodity', 'market', 'price']].rename(columns={
        'market': 'Market (Lowest)',
        'price': 'Lowest Price'
    })

    min_df = pd.merge(min_df, national_avg, on='commodity', how='left')

    # Display
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"<h4 style='color:green;'> Lowest Food Prices in {selected_month}</h4>", unsafe_allow_html=True)
        st.dataframe(min_df)

    with col2:
        st.markdown(f"<h4 style='color:red;'> Highest Food Prices in {selected_month}</h4>", unsafe_allow_html=True)
        st.dataframe(max_df)
        
    

    # Page setup
    st.title(" Monthly Food Price Highlights")

    # Dropdown to select year and month
    selected_period = st.selectbox(
        "Select Year and Month",
        sorted(df['year_month'].unique()),
        key="selectbox_year_month"
    )


    # Filter data by selected year and month
    filtered_df = df[df['year_month'] == selected_period]

    # Step 3: Get categories available for this period
    available_categories = sorted(filtered_df['category'].dropna().unique())

    # Step 4: Multiselect only shows valid categories for selected period
    selected_categories = st.multiselect(
        "Select Food Categories",
        available_categories,
        default=available_categories
    )


    # Step 5: Filter further by selected categories
    filtered_df = filtered_df[filtered_df['category'].isin(selected_categories)]

    # Step 6: Display data or warning
    if filtered_df.empty:
        st.warning("No data available for the selected filters.")
    else:
        # Highest price info
        highest = filtered_df.loc[filtered_df['price'].idxmax()]
        # Lowest price info
        lowest = filtered_df.loc[filtered_df['price'].idxmin()]
        # National average
        national_avg = filtered_df[filtered_df['market'] == 'National Average']['price'].mean()


    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label=" Highest Price", value=f"Rs. {highest['price']:.2f}",
                  delta=f"{highest['commodity']} at {highest['market']}")

    with col2:
        st.metric(label=" Lowest Price", value=f"Rs. {lowest['price']:.2f}", 
                  delta=f"{lowest['commodity']} at {lowest['market']}")

    with col3:
        st.metric(label="🇱🇰 National Average", value=f"Rs. {national_avg:.2f}", 
                  delta=f"For {selected_period}")
    st.title(" Price Changes Over Time")
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
        st.subheader(f" Price Trends for {selected_category} ({selected_saletype})")

        # ---- Build a Plotly line chart ---------------------------------------------
        if selected_commodities:
            line_df = filtered_df[filtered_df['commodity'].isin(selected_commodities)]

            fig = px.line(
                line_df,
                x='date',
                y='price',
                color='commodity',
                labels={
                    'date': 'Date',
                    'price': 'Price (LKR)',
                    'commodity': 'Food Item'
                },
                title=f"Price Changes Over Time – {selected_category}",
                height=550
            )
    

            # Optional layout tweaks
            fig.update_layout(
                legend_title_text='Food Item',
                hovermode='x unified',          # single hover box per x‑value
                margin=dict(l=30, r=30, t=60, b=30)
            )

            st.plotly_chart(fig, use_container_width=True)

        else:st.info("Select at least one food item to see the price trend.")
    
    
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
        "<p style='font-size:18px; color:orange;'> Summary Statistics</p>",
        unsafe_allow_html=True
        )

         
    
        st.dataframe(df.describe())
    # ---- Column 2: DataFrame Info ----
    with col2:
        st.markdown(
        "<p style='font-size:18px; color:orange;'> Dataset Info</p>",
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
            "<p style='font-size:18px; color:orange; font-weight:bold;'> Missing Values</p>",
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
                    No missing values found 
                </div>
                """,
                unsafe_allow_html=True
            )
        

if page == "About":
    import os

    # --- Page Title ---
    st.title(" About Food Categories")

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
    st.markdown(f"###  Food Items in {selected_category}:")
    food_items = df[df['category'] == selected_category]['commodity'].dropna().unique()
    styled_food_items = f"""
    <div style='font-size:17px; color:#1e3d59; background-color:#f9f9f9; padding: 15px; border-left: 5px solid #ff914d; border-radius: 8px;'>
        {", ".join(sorted(food_items))}
    </div>
    """
    st.markdown(styled_food_items, unsafe_allow_html=True)

    st.markdown("###  Price Distribution Map by Category & Commodity")

    # --- Unique Categories ---
    categories = df['category'].dropna().unique()

    # --- Select Box for Category with unique key ---
    selected_category = st.selectbox(
        "Select a Food Category", 
        sorted(categories), 
        key="category_select"
    )


    # --- Filter commodities based on selected category ---
    filtered_df = df[df['category'] == selected_category]
    commodities = filtered_df['commodity'].dropna().unique()

    # --- Select Box for Commodity (within selected category) with unique key ---
    selected_commodity = st.selectbox(
         "Select a Food Item (Commodity)", 
        sorted(commodities), 
        key="commodity_select"
    )


    # --- Filter data for the map ---
    map_df = filtered_df[
        (filtered_df['commodity'] == selected_commodity) &
        (filtered_df['latitude'].notna()) &
        (filtered_df['longitude'].notna()) &
        (filtered_df['price'].notna())
    ]


    # --- Show the map ---
    if not map_df.empty:
        fig_map = px.scatter_map(
        map_df,
        lat="latitude",
        lon="longitude",
        color="category",
        size="price",
        hover_name="commodity",
        hover_data=["market", "price"],
        zoom=6,
        height=550,
        title=f" Price Distribution for {selected_commodity.title()} in {selected_category.title()}",
        )
    
        fig_map.update_layout(mapbox_style="carto-positron")
        fig_map.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})
        st.plotly_chart(fig_map)
    else:
        st.info("No map data available for this combination.")

            





