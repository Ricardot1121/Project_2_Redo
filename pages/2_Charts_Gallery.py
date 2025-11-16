# pages/2_Charts_Gallery.py
import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------------------------
# Page Title
# -----------------------------------------------------------
st.title("📊 EDA Gallery — USA Accidents Sample")

# -----------------------------------------------------------
# Load Data
# -----------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/accidents_small.csv")

df = load_data()
st.write(f"Dataset rows: {len(df)}")
st.write(f"Available columns: {', '.join(df.columns)}")

# -----------------------------------------------------------
# Sidebar Filters
# -----------------------------------------------------------
st.sidebar.header("Filters")

states = sorted(df['State'].dropna().unique())
selected_states = st.sidebar.multiselect("Select States", states, default=states[:5])

# Temperature range filter (since we have Temperature(F))
temp_min = float(df['Temperature(F)'].min()) if not df['Temperature(F)'].isna().all() else 0
temp_max = float(df['Temperature(F)'].max()) if not df['Temperature(F)'].isna().all() else 100
selected_temp_range = st.sidebar.slider("Temperature Range (°F)", temp_min, temp_max, (temp_min, temp_max))

filtered_df = df[
    (df['State'].isin(selected_states)) & 
    (df['Temperature(F)'].between(selected_temp_range[0], selected_temp_range[1]))
]

# -----------------------------------------------------------
# 1) Bar Chart — Accidents by State
# -----------------------------------------------------------
st.subheader("1) Accidents by State")
st.write("Question: Which states have the most accidents in the selected sample?")

state_counts = filtered_df['State'].value_counts().reset_index()
state_counts.columns = ['State', 'Count']

fig_bar = px.bar(
    state_counts,
    x='Count',
    y='State',
    orientation='h',
    text='Count',
    labels={'Count': 'Number of Accidents', 'State': 'State'},
    title='Accidents by State'
)
fig_bar.update_layout(yaxis={'categoryorder': 'total ascending'})

st.plotly_chart(fig_bar, use_container_width=True)

with st.expander("How to read this chart"):
    st.write("""
    - Y axis: State abbreviations  
    - X axis: Number of accidents  
    - Bars ordered by accident count  
    - Hover to see exact numbers
    """)

st.markdown("**Observations:**")
st.write("""
- Some states have more recorded accidents than others.  
- Counts reflect the sample and reporting; interpret with caution.  
- Useful for identifying high-accident regions in this dataset.
""")

st.markdown("---")

# -----------------------------------------------------------
# 2) Histogram — Temperature Distribution
# -----------------------------------------------------------
st.subheader("2) Temperature Distribution")
st.write("Question: How are accident temperatures distributed?")

fig_hist = px.histogram(
    filtered_df.dropna(subset=['Temperature(F)']),
    x='Temperature(F)',
    nbins=30,
    labels={'Temperature(F)': 'Temperature (°F)'},
    title='Temperature Distribution of Accidents'
)
st.plotly_chart(fig_hist, use_container_width=True)

with st.expander("How to read this chart"):
    st.write("""
    - X axis: Temperature in Fahrenheit  
    - Y axis: Number of accidents  
    - Shows the distribution of temperatures when accidents occurred  
    - Filter selections in the sidebar affect this chart
    """)

st.markdown("**Observations:**")
st.write("""
- Most accidents occur in moderate temperature ranges.  
- Extreme temperatures (very hot or cold) may have fewer accidents.  
- Temperature filtering affects the distribution shape.
""")

st.markdown("---")

# -----------------------------------------------------------
# 3) Scatter Plot — Location Map
# -----------------------------------------------------------
st.subheader("3) Accidents by Location")
st.write("Question: Where do accidents occur geographically?")

# Sample data for performance if too many points
map_df = filtered_df.dropna(subset=['Start_Lat', 'Start_Lng'])
if len(map_df) > 1000:
    map_df = map_df.sample(n=1000, random_state=42)

fig_map = px.scatter_mapbox(
    map_df,
    lat='Start_Lat',
    lon='Start_Lng',
    color='Temperature(F)',
    hover_data=['City', 'State', 'Start_Time', 'Temperature(F)'],
    color_continuous_scale=px.colors.sequential.Viridis,
    size_max=15,
    zoom=3,
    title='Accident Locations (Sample)',
    labels={'Temperature(F)': 'Temperature (°F)'}
)

fig_map.update_layout(mapbox_style="open-street-map")
fig_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

st.plotly_chart(fig_map, use_container_width=True)

with st.expander("How to read this chart"):
    st.write("""
    - Each dot represents an accident location (sampled for performance)  
    - Color indicates temperature at time of accident  
    - Hover to see city, state, time, and temperature  
    - Warmer colors = higher temperatures
    """)

st.markdown("**Observations:**")
st.write("""
- Geographic distribution shows accident hotspots.  
- Color coding reveals temperature patterns by location.  
- Clustering may indicate high-traffic areas or weather patterns.
""")

st.markdown("---")

# -----------------------------------------------------------
# 4) Time Series — Accidents Over Time
# -----------------------------------------------------------
st.subheader("4) Accidents Over Time")
st.write("Question: When do accidents occur most frequently?")

# Convert Start_Time to datetime with error handling
time_df = filtered_df.copy()
try:
    time_df['Start_Time'] = pd.to_datetime(time_df['Start_Time'], errors='coerce')
    # Remove rows where datetime conversion failed
    time_df = time_df.dropna(subset=['Start_Time'])
    
    if len(time_df) > 0:
        time_df['Date'] = time_df['Start_Time'].dt.date
        
        # Group by date
        daily_counts = time_df.groupby('Date').size().reset_index(name='Accidents')
        daily_counts['Date'] = pd.to_datetime(daily_counts['Date'])
        
        fig_time = px.line(
            daily_counts,
            x='Date',
            y='Accidents',
            title='Daily Accident Counts Over Time'
        )
        
        st.plotly_chart(fig_time, use_container_width=True)
    else:
        st.warning("No valid dates found for time series analysis.")
        
except Exception as e:
    st.error(f"Error processing dates: {str(e)}")
    st.info("Skipping time series chart due to date format issues.")

with st.expander("How to read this chart"):
    st.write("""
    - X axis: Date  
    - Y axis: Number of accidents per day  
    - Shows temporal patterns in accident frequency  
    - Peaks may indicate specific events or seasonal patterns
    """)

st.markdown("**Observations:**")
st.write("""
- Time series reveals patterns in accident frequency.  
- Seasonal or weekly patterns may be visible.  
- Filtering by state and temperature affects temporal trends.
""")
