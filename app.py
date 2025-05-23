import streamlit as st
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns 
import plotly.graph_objects as go
from streamlit_extras.metric_cards import style_metric_cards
from io import BytesIO
# Set page config to use the full width
st.set_page_config(layout="wide")
st.title(" Food Price Changes In Sri Lanka Over the Time")
#import dataset
df = pd.read_csv("SL_FoodPriceChanges.csv")
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Sidebar
st.sidebar.title("CONTENT")
page = st.sidebar.selectbox("Choose a page", ["About","Overview","Price Trends" ,"Economic centres VS National Average"])
st.markdown(
    """
    <style>
        /* Global dark background and light text */
        body {
            background-color: #0E1117;
            color: #FAFAFA;
        }

        /* Container style */
        .main {
            background-color: #0E1117;
            color: #FAFAFA;
        }

        /* Headings */
        h1, h2, h3, h4, {
            color: #F39C12;
        }

        /* Input widgets */
        .stSelectbox, .stTextInput, .stDateInput, .stMultiSelect, .stNumberInput {
            background-color: #1C1C1C !important;
            color: #FAFAFA !important;
        }

        /* Table and dataframe */
        .stDataFrame {
            background-color: #1E1E1E;
        }

        /* Sidebar (optional) */
        .css-1d391kg { 
            background-color: #1C1C1C; 
            color: #FAFAFA;
        }

        /* Line chart bg */
        .stPlotlyChart {
            background-color: #1E1E1E;
        }

        /* Buttons */
        .stButton > button {
            background-color: #F39C12;
            color: white;
            font-weight: bold;
        }

        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #2E2E2E;
        }
        ::-webkit-scrollbar-thumb {
            background: #F39C12;
            border-radius: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)



if page == "Price Trends":
    st.sidebar.header("Price Trend Over Time")

      # Filter: Category
    categories = df['category'].dropna().unique()
    selected_category = st.sidebar.selectbox("Select Food Category", sorted(categories))

    # Filter: Commodity based on selected category
    filtered_commodities = df[df['category'] == selected_category]['commodity'].dropna().unique()
    selected_commodity = st.sidebar.selectbox("Select Food Name", sorted(filtered_commodities))

    # Filter: Price Type
    sale_types = df['pricetype'].dropna().unique()
    selected_saletype = st.sidebar.selectbox("Select Price Type", sorted(sale_types))

    # Filter: District
    districts = df['District'].dropna().unique()
    selected_district = st.sidebar.selectbox("Select District", sorted(districts))

    # --- Apply filters ---
    filtered_df = df[
        (df['category'] == selected_category) &
        (df['commodity'] == selected_commodity) &
        (df['pricetype'] == selected_saletype) &
        (df['District'] == selected_district)
    ]

    # --- Show Table ---
    st.markdown(
        f"###  Prices for {selected_commodity} ({selected_saletype}) in {selected_category} - {selected_district}",
        unsafe_allow_html=True
    )
    

    
    st.markdown(
        "<h3 style='color: orange;'> Price Trend Over Time</h3>",
        unsafe_allow_html=True
    )

    if 'date' in filtered_df.columns and 'price' in filtered_df.columns and not filtered_df.empty:
        price_chart_data = (
            filtered_df.groupby('date')['price']
            .mean()
            .reset_index()
            .sort_values('date')
        )
        fig = go.Figure()

        # Actual price line
        fig.add_trace(go.Scatter(
            x=price_chart_data['date'],
            y=price_chart_data['price'],
            mode='lines',
            name=f'{selected_commodity} Price',
            line=dict(color='blue')
        ))
        # Rolling 30-day Mean
        if len(price_chart_data) >= 30:
            price_chart_data['rolling_mean'] = price_chart_data['price'].rolling(window=30).mean()
            fig.add_trace(go.Scatter(
                x=price_chart_data['date'],
                y=price_chart_data['rolling_mean'],
                mode='lines',
                name='30-day Rolling Average',
                line=dict(color='red')
            ))
        # Highlight Special Periods (optional)
        fig.add_vrect(
            x0="2018-06-01", x1="2018-10-01",
            fillcolor="red", opacity=0.2,
            layer="below", line_width=0,
        )
        fig.add_vrect(
            x0="2019-06-01", x1="2019-09-01",
            fillcolor="red", opacity=0.2,
            layer="below", line_width=0,
        )

        # Customize layout
        fig.update_layout(
            title=f"{selected_commodity} ({selected_saletype}) Price Trend in {selected_district}",
            xaxis_title="Date",
            yaxis_title="Price (LKR)",
            hovermode="x unified",
            height=600,
            margin=dict(l=20, r=20, t=50, b=20),
            template="plotly_white",
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(count=5, label="5y", step="year", stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(visible=True), 
                type="date"
            )
        )   
        
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("No data available for the selected filters. Please try different options.")
    st.dataframe(filtered_df)
    

    

    df['year_month'] = df['date'].dt.to_period('M').astype(str)

   
    available_months = sorted(df['year_month'].dropna().unique())
    selected_period = st.sidebar.selectbox("Select Year-Month", available_months)

    
    st.markdown("###  Filter by Time Period and Category")

    col_filter1, col_filter2 = st.columns(2)

    with col_filter1:
        selected_period = st.selectbox("Select Year-Month", sorted(df['year_month'].dropna().unique()), index=0, key="year_month_selectbox")

    with col_filter2:
        selected_category = st.selectbox("Select Food Category", sorted(df['category'].dropna().unique()),key="category_selectbox")

    
    df_month = df[(df['year_month'] == selected_period) & (df['category'] == selected_category)]


    
    national_avg = (
        df_month[df_month['market'] == "National Average"]
        .groupby('commodity')['price']
        .mean()
        .reset_index()
        .rename(columns={'price': 'National Average Price'})
    )

    
    max_prices = df_month.loc[df_month.groupby('commodity')['price'].idxmax()]
    max_df = max_prices[['commodity', 'market', 'price']].rename(columns={
        'market': 'Market (Highest)',
        'price': 'Highest Price'
    })


    max_df = pd.merge(max_df, national_avg, on='commodity', how='left')

    
    min_prices = df_month.loc[df_month.groupby('commodity')['price'].idxmin()]
    min_df = min_prices[['commodity', 'market', 'price']].rename(columns={
        'market': 'Market (Lowest)',
        'price': 'Lowest Price'
    })

    min_df = pd.merge(min_df, national_avg, on='commodity', how='left')

    
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"<h4 style='color:green;'>Lowest Food Prices in {selected_period} ({selected_category})</h4>", unsafe_allow_html=True)
        st.dataframe(min_df)

    with col2:
        st.markdown(f"<h4 style='color:red;'>Highest Food Prices in {selected_period} ({selected_category})</h4>", unsafe_allow_html=True)
        st.dataframe(max_df)

        
    

    
    st.title(" Monthly Food Price Highlights")

    
    selected_period = st.selectbox(
        "Select Year and Month",
        sorted(df['year_month'].unique()),
        key="selectbox_year_month"
    )


    
    filtered_df = df[df['year_month'] == selected_period]

    
    available_categories = sorted(filtered_df['category'].dropna().unique())

    
    selected_categories = st.multiselect(
        "Select Food Categories",
        available_categories,
        default=available_categories
    )


    
    filtered_df = filtered_df[filtered_df['category'].isin(selected_categories)]

   
    if filtered_df.empty:
        st.warning("No data available for the selected filters.")
    else:
        # Highest price 
        highest = filtered_df.loc[filtered_df['price'].idxmax()]
        # Lowest price 
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
    st.sidebar.header("Price Changes Over Time")

    

    
    categories = df['category'].dropna().unique()
    selected_category = st.sidebar.selectbox("Select Food Category", sorted(categories),key="category_selectbox_1")

    
    filtered_commodities = df[df['category'] == selected_category]['commodity'].dropna().unique()
    selected_commodities = st.sidebar.multiselect("Select Food Items", sorted(filtered_commodities),key="commodity_multiselect")

    
    sale_types = df['pricetype'].dropna().unique()
    selected_saletype = st.sidebar.selectbox("Select Price Type", sorted(sale_types),key="pricetype_selectbox")

    
    filtered_df = df[
        (df['category'] == selected_category) &
        (df['commodity'].isin(selected_commodities)) &
        (df['pricetype'] == selected_saletype) 
    ]


    
    if not selected_commodities:
        st.warning("Please select at least one food item to view the price trend.")
    elif filtered_df.empty:
        st.info("No data available for the selected filters.")
    else:
        st.subheader(f"Price Trends for {selected_category} ({selected_saletype})")

        line_df = filtered_df[filtered_df['commodity'].isin(selected_commodities)]

        pivot_df = line_df.pivot_table(
            index='date',
            columns='commodity',
            values='price',
            aggfunc='mean'
        )

        pivot_df = pivot_df.sort_index()

        
        pivot_reset_df = pivot_df.reset_index()
        melted_df = pivot_reset_df.melt(id_vars='date', var_name='Food Item', value_name='Price')

        fig = px.line(
            melted_df,
            x='date',
            y='Price',
            color='Food Item',
            title=f" Price Comparison Over Time – {selected_category} ({selected_saletype})",
            labels={"date": "Date", "Price": "Price (LKR)", "Food Item": "Commodity"}
        )


        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Price (LKR)",
            legend_title="Food Item",
            hovermode="x unified"
        )


        st.plotly_chart(fig, use_container_width=True)
    
    # Create year_range column
    def assign_year_range(x):
        if x.year >= 2004 and x.year < 2009:
            return '2004-2009'
        elif x.year >= 2009 and x.year < 2014:
            return '2009-2014'
        elif x.year >= 2014 and x.year < 2019:
            return '2014-2019'
        elif x.year >= 2019 and x.year <= 2025:
            return '2019-2025'
        else:
            return 'Other'

    df['year_range'] = df['date'].apply(assign_year_range)
    st.subheader(" Food Category Records Across Time Ranges")

    
    range_category = df.groupby(['year_range', 'category']).size().reset_index(name='counts')

    
    fig3 = px.bar(
        range_category,
        x='year_range',
        y='counts',
        color='category',
        title="Number of Food Categories Recorded Across Different Year Ranges",
        labels={'year_range': 'Year Range', 'counts': 'Number of Records', 'category': 'Food Category'},
        barmode='stack'
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("## Records per Food Category")
    category_counts = df['category'].value_counts().reset_index()
    category_counts.columns = ['Category', 'Count']

    fig_bar = px.bar(
        category_counts,
        x='Count',
        y='Category',
        orientation='h',
        color='Count',
        color_continuous_scale='Viridis',
        title="Number of Records per Food Category",
        labels={'Count': 'Number of Records', 'Category': 'Food Category'}
    )

    fig_bar.update_layout(yaxis=dict(categoryorder='total ascending'))

    st.plotly_chart(fig_bar, use_container_width=True)

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['year_month'] = df['date'].dt.to_period('M').astype(str)

   
    st.markdown("## Filter Options")

    col1, col2, col3 = st.columns(3)
    with col1:
        categories = df['category'].dropna().unique()
        selected_category = st.selectbox("Select Food Category", sorted(categories), key='top_category')

    with col2:
        price_types = df['pricetype'].dropna().unique()
        selected_price_type = st.selectbox("Select Price Type", sorted(price_types), key='top_price_type')

    
    with col3:
        year_ranges = {
            "2004-2009": (2004, 2009),
            "2009-2014": (2009, 2014),
            "2014-2019": (2014, 2019),
            "2019-2025": (2019, 2025),
        }
        selected_range = st.selectbox("Select Year Range", list(year_ranges.keys()), key='top_year_range')
        start_year, end_year = year_ranges[selected_range]

    # Filter by year range
    df['year'] = df['date'].dt.year
    filtered_df = df[
        (df['category'] == selected_category) &
        (df['commodity'].isin(selected_commodities)) &
        (df['pricetype'] == selected_price_type) &
        (df['year'] >= start_year) &
        (df['year'] < end_year)
    ]

    st.markdown("###  Highest & Lowest Priced Items by Month")
    month_df = df[
        (df['pricetype'] == selected_price_type) &
        (df['category'] == selected_category)
        ].copy()
    month_df = month_df.groupby(['year_month', 'commodity'])['price'].mean().reset_index()

    max_price_df = month_df.loc[month_df.groupby('year_month')['price'].idxmax()]
    min_price_df = month_df.loc[month_df.groupby('year_month')['price'].idxmin()]

    col1, col2 = st.columns(2)

    with col1:
        fig_max = px.bar(max_price_df, x='year_month', y='price', color='commodity',
                         title="Monthly Highest Price Items", labels={'price': 'Price (LKR)', 'year_month': 'Month'})
        st.plotly_chart(fig_max, use_container_width=True)

    with col2:
        fig_min = px.bar(min_price_df, x='year_month', y='price', color='commodity',
                         title="Monthly Lowest Price Items", labels={'price': 'Price (LKR)', 'year_month': 'Month'})
        st.plotly_chart(fig_min, use_container_width=True)

    
    st.markdown("###  Category Distribution")
    cat_pie = df[df['category'] == selected_category]['commodity'].value_counts().reset_index()
    cat_pie.columns = ['commodity', 'count']
    fig2 = px.pie(cat_pie, names='commodity', values='count', title=f'Commodity Distribution in {selected_category}')
    st.plotly_chart(fig2, use_container_width=True)  


    df['year_month'] = df['date'].dt.to_period('M').astype(str)
    df['year'] = df['date'].dt.year
    year_ranges = {
        "2004-2009": (2004, 2009),
        "2009-2014": (2009, 2014),
        "2014-2019": (2014, 2019),
        "2019-2025": (2019, 2025),
    }
    
    st.title(" Overview of Food Prices")
    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        selected_range = st.selectbox("Select Year Range", list(year_ranges.keys()),key="year_range_select")
    with col_filter2:
        categories = df['category'].dropna().unique()
        selected_category = st.selectbox("Select Food Category", sorted(categories),key="category_select")

    # Filter Data
    start_year, end_year = year_ranges[selected_range]
    filtered_df = df[(df['year'] >= start_year) & (df['year'] < end_year)]
    filtered_df = filtered_df[filtered_df['category'] == selected_category]
    # Top Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label=" Highest Price", value=f"LKR {filtered_df['price'].max():,.2f}")
    with col2:
        st.metric(label=" Lowest Price", value=f"LKR {filtered_df['price'].min():,.2f}")
    with col3:
        st.metric(label=" Average Price", value=f"LKR {filtered_df['price'].mean():,.2f}")
        style_metric_cards(
        background_color="#1f2229", 
        border_left_color="#00FFFF", 
        border_color="#00FFFF"
        )
    # Trend Line Chart
    st.subheader(" Average Price Trend Over Time")
    trend_df = filtered_df.groupby('year_month')['price'].mean().reset_index()
    fig = px.line(
        trend_df, x='year_month', y='price',
        labels={'price': 'Average Price (LKR)', 'year_month': 'Year-Month'},
        markers=True,
        template="plotly_dark",
        title="Average Monthly Food Price"
    )
    fig.update_traces(line_color='#00FFFF')
    fig.update_layout(margin=dict(l=20, r=20, t=60, b=20))
    st.plotly_chart(fig, use_container_width=True)
    
if page == "Overview":
    st.write("Here's the dataset:")
    st.dataframe(df)
    

    st.markdown(
        "<p style='font-size:22px; color:White;'>Overview:</p>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='font-size:18px; color:orange;'>Here's the first few rows of dataset (After Preparation):</p>",
        unsafe_allow_html=True
    )
    
    st.dataframe(df.head())
    st.markdown(
        """
        <br>
        <p style='font-size:18px; color:orange;'> Data Preparation Steps:</p>
        <ul style='font-size:16px; color:white;'>
            <li> Imputed missing values in key columns to ensure data completeness.</li>
            <li> Converted column data types (e.g., date fields to datetime).</li>
            <li> Removed irrelevant rows and outlier records based on domain knowledge.</li>
            <li> Renamed columns for clarity and consistency.</li>
            <li> Filtered dataset to include only selected economic centers and relevant categories.</li>
            <li> Ensured consistency in category and market names for easier filtering and analysis.</li>
        </ul>
        """,
        unsafe_allow_html=True
    )

    
    
    
    col1, col2, col3 = st.columns(3)

    
    with col1:
        st.markdown(
        "<p style='font-size:18px; color:orange;'> Summary Statistics</p>",
        unsafe_allow_html=True
        )

         
    
        st.dataframe(df.describe())
    
    with col2:
        st.markdown(
        "<p style='font-size:18px; color:orange;'> Dataset Info</p>",
        unsafe_allow_html=True
        )
    

        
        info_table = pd.DataFrame({
            'Column': df.columns,
            'Non-Null Count': df.notnull().sum().values,
            'Dtype': df.dtypes.values
        })

       
        info_table.reset_index(drop=True, inplace=True)

        
        st.dataframe(info_table)

    
    with col3:
        
        st.markdown(
            "<p style='font-size:18px; color:orange; font-weight:bold;'> Missing Values</p>",
            unsafe_allow_html=True
        )

        
        missing_counts = df.isnull().sum()
        missing_df = missing_counts[missing_counts > 0].reset_index()
        missing_df.columns = ['Column', 'Missing Values']

        if not missing_df.empty:
            
            st.dataframe(missing_df)
        else:
            
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
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1649067846117-2d71b76be1e0?q=80&w=2011&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>
        .big-title {
            -size: 40px;
            font-weight: bold;
            color: white;
            text-shadow: 2px 2px 6px rgba(0,0,0,0.7);
            margin-bottom: 10px;
        }   
        .sub-heading {
            font-size: 20px;
            color: white;
            text-shadow: 1px 1px 4px rgba(0,0,0,0.6);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="big-title">Food Price Changes In Sri Lanka Over the Time</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-heading">Welcome to the Sri Lanka Food Price Dashboard.<br>This platform helps visualize food price variations across major economic centers. Explore insights, trends, and market-specific details.</div>', unsafe_allow_html=True)



    
    st.title(" About Food Categories")

    

    
    categories = df['category'].dropna().unique()

    
    selected_category = st.selectbox("Select a Food Category", sorted(categories))

    
    category_descriptions = {
        "cereals and tubers": "Cereals like rice, wheat, and maize, along with tubers such as potatoes, yams, and cassava, form the backbone of diets across the world. They are primary sources of complex carbohydrates, providing energy, dietary fiber, and essential nutrients. These staples are not just filling—they're foundational to food security and cultural cuisines.",
        "meat, fish and eggs": "This category delivers high-quality proteins crucial for muscle development, hormone production, and immune function. Meat and fish offer important nutrients like iron, zinc, and omega-3 fatty acids, while eggs are a powerhouse of vitamins and healthy fats. Together, they form a cornerstone of many balanced diets.",
        "miscellaneous food": "This diverse category includes a mix of food items that don't strictly belong to the main groups—ranging from processed foods, snacks, and condiments to specialty ingredients. Though varied, these foods often enhance flavor, convenience, and cultural diversity in diets when consumed in moderation.",
        "oil and fats": "Oils and fats—whether from plants like coconut and sunflower or animal sources like ghee and butter—play a vital role in flavor, texture, and nutrition. They provide essential fatty acids, aid in the absorption of fat-soluble vitamins (A, D, E, K), and serve as a dense source of energy. Used wisely, they support both culinary richness and health.",
        "pulses and nuts": "A powerhouse of plant-based nutrition, pulses (like lentils, beans, and chickpeas) and nuts (like cashews and almonds) are rich in protein, fiber, and heart-healthy fats. They contribute to sustainable diets and are a vital source of nutrients for vegetarians and vegans.",
        "vegetables and fruits": "Colorful, vibrant, and nutrient-dense—fruits and vegetables are the champions of health. They are loaded with essential vitamins, minerals, antioxidants, and fiber that help prevent disease, support digestion, and boost immunity. A diverse intake is key to overall well-being and vitality."
    }


    
    category_images = {
        "cereals and tubers": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSGoG0zWA2Swi132IwbXh9if8EoaR1bgYHEuw&s",
        "meat, fish and eggs": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRYLm0THhvanao7aWofOQzflpos3T_W2VEvyQ&s",
        "miscellaneous food": "https://thumbs.dreamstime.com/b/close-up-chopped-hot-chili-peppers-heaps-salt-sugar-garlic-allspice-bay-leaf-old-wooden-surface-selective-close-up-156240684.jpg",
        "oil and fats": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQBK51naBmSGfzjapHrjdDI7W6QP6WbHUkELg&s",
        "pulses and nuts": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQYgOa8tQlXNO7l37zGMF7I-dKWd96SmX2H-Q&s",
        "vegetables and fruits": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQOGpxLJbhDOSQ8HoXlJmUnvt8PTSN5HKApRw&s"
    }


    
    styled_description = f"""
    <div style='font-size:18px; color:#2c3e50; background-color:#f0f8ff; padding: 15px; border-radius: 10px;'>
       {category_descriptions.get(selected_category, "No description available.")}
    </div>
    """
    st.markdown(styled_description, unsafe_allow_html=True)

    st.image(category_images.get(selected_category, ""), caption=selected_category, width=350)
    

    
    st.markdown(f"###  Food Items in {selected_category}:")
    food_items = df[df['category'] == selected_category]['commodity'].dropna().unique()
    styled_food_items = f"""
    <div style='font-size:17px; color:#1e3d59; background-color:#f9f9f9; padding: 15px; border-left: 5px solid #ff914d; border-radius: 8px;'>
        {", ".join(sorted(food_items))}
    </div>
    """
    st.markdown(styled_food_items, unsafe_allow_html=True)

    st.markdown("###  Price Distribution Map by Category & Commodity")

    
    categories = df['category'].dropna().unique()

   
    selected_category = st.selectbox(
        "Select a Food Category", 
        sorted(categories), 
        key="category_select"
    )


    
    filtered_df = df[df['category'] == selected_category]
    commodities = filtered_df['commodity'].dropna().unique()

    
    selected_commodity = st.selectbox(
         "Select a Food Item (Commodity)", 
        sorted(commodities), 
        key="commodity_select"
    )
  
    map_df = filtered_df[
        (filtered_df['commodity'] == selected_commodity) &
        (filtered_df['latitude'].notna()) &
        (filtered_df['longitude'].notna()) &
        (filtered_df['price'].notna())
    ].copy()
    economic_centers = ["Economic Centre-Dambulla","Economic Centre - Peliyagoda","Economic Centre-Pettah","Fish market-Peliyagoda","Fish market-Negombo","Economic Centre-Maradagahamula"]
    

    map_df['highlight'] = map_df['market'].apply(lambda x: 'Key Center' if x.strip().lower() in [ec.lower() for ec in economic_centers] else 'Other Market')
    color_map = {
        'economic centers': 'blue',
        'Other Market': 'red'
    }
    if not map_df.empty:
        fig_map = px.scatter_map(
        map_df,
        lat="latitude",
        lon="longitude",
        color="market",
        color_discrete_map=color_map,
        size="price",
        hover_name="commodity",
        hover_data=["market", "price"],
        zoom=6,
        height=550,
        title=f"Price Distribution for {selected_commodity.title()} in {selected_category.title()}",
        )
    
        fig_map.update_layout(mapbox_style="carto-positron")
        fig_map.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})
        st.plotly_chart(fig_map)
    else:
        st.info("No map data available for this combination.")


    
if page == "Economic centres VS National Average":
       st.title("Economic Centers vs National Average")
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

    
       category_df = filtered_df[filtered_df['category'] == selected_category]
       price_comparison = category_df.groupby('market')['price'].mean()
       national_avg = price_comparison.get('National Average', None)
       market_prices = price_comparison.drop('National Average', errors='ignore')
       bar_df = (
           market_prices.reset_index(name='Economic Center Price')
           .rename(columns={'market': 'Economic Center'})
       )
       bar_df['National Average'] = national_avg
       bar_df = bar_df.melt(
           id_vars='Economic Center',
           var_name='Series',
           value_name='Average Price'
       )


    
       fig_bar = px.bar(
           bar_df,
           x='Economic Center',
           y='Average Price',
           color='Series',
           barmode='group',                 
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


       national_df = df[df['market'] == 'National Average'].copy()
       national_df['date'] = pd.to_datetime(national_df['date'])
       national_avg_trend = national_df.groupby(['date', 'commodity'])['price'].mean().reset_index()
       available_na_commodities = national_avg_trend['commodity'].unique()
       selected_na_commodity = st.selectbox(
           " Select Food Item (National Average only)",
           sorted(available_na_commodities),
           key="na_commodity"
       )
       na_filtered = national_avg_trend[national_avg_trend['commodity'] == selected_na_commodity]
       st.subheader(f" National Average Trend for {selected_na_commodity}")
       fig = px.line(
           na_filtered,
           x='date',
           y='price',
           title=f"National Average Price Over Time – {selected_na_commodity}",
           labels={"date": "Date", "price": "Price (LKR)"}
       )
       fig.update_layout(hovermode='x unified', height=500)
       st.plotly_chart(fig, use_container_width=True)


       st.markdown("###  National Average Prices (Filtered Dates Only)")
       st.dataframe(na_filtered.sort_values(by="date", ascending=False), use_container_width=True)

       centers = [
           'Economic Centre-Dambulla',
           'Economic Centre - Peliyagoda',
           'Economic Centre-Pettah',
           'Fish market-Peliyagoda',
           'Fish market-Negombo',
           'Economic Centre-Maradagahamula'
       ]
       center_descriptions = {
            'Economic Centre-Dambulla': "A major agricultural hub supplying central and northern regions.",
            'Economic Centre - Peliyagoda': "Key wholesale market close to Colombo, handling both vegetables and fruits.",
            'Economic Centre-Pettah': "Busy trade center located in the heart of Colombo city.",
            'Fish market-Peliyagoda': "Primary wholesale fish market servicing Colombo and suburbs.",
            'Fish market-Negombo': "Coastal market known for a variety of seafood.",
            'Economic Centre-Maradagahamula': "Local trade center facilitating produce from surrounding rural areas."
       }
       selected_center = st.sidebar.selectbox("Select an Economic Center", centers)
       center_data = df[df['market'] == selected_center]
       st.markdown(f"##  {selected_center}")
       st.write(center_descriptions.get(selected_center, "Description not available."))
       if not center_data.empty:
        st.markdown("###  Commodity Prices Overview")
        commodity_stats = center_data.groupby('commodity')['price'].agg(['mean', 'min', 'max']).round(2).reset_index()
        fig = px.bar(commodity_stats, x='commodity', y='mean',
                     title=f"Average Prices by Commodity in {selected_center}",
                     color='commodity', height=500)
        st.plotly_chart(fig)
        fig2 = px.bar(commodity_stats, x='commodity', y=['min', 'max'],
              title=f"Minimum and Maximum Prices by Commodity in {selected_center}",
              barmode='group', height=500,
              labels={'value': 'Price', 'variable': 'Price Type'})
        st.plotly_chart(fig2)
       else:
        st.warning("No data available for this economic center.")
