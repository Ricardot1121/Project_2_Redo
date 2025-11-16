# 2_📊_Charts_Gallery.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="EDA Gallery", page_icon="📊")

st.title("📊 EDA Gallery — USA Accidents Sample")

# ----------------------------
# Load Data
# ----------------------------
@st.cache_data
def load_data():
    return pd.read_parquet("data/accidents_small.parquet")

df = load_data()
st.write(f"Dataset rows: {len(df)}")

# ----------------------------
# Sidebar Filters (shared for multiple charts)
# ----------------------------
st.sidebar.header("Filters")
states = sorted(df['State'].dropna().unique())
selected_states = st.sidebar.multiselect("Select States", states, default=states[:5])

severity_values = sorted(df['Severity'].dropna().unique())
selected_severity = st.sidebar.multiselect("Select Severity", severity_values, default=severity_values)

filtered_df = df[(df['State'].isin(selected_states)) & (df['Severity'].isin(selected_severity))]

# ----------------------------
# 1) Bar Chart — Accidents by State
# ----------------------------
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
    labels={'Count':'Number of Accidents', 'State':'State'},
    title='Accidents by State'
)
fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})

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

# ----------------------------
# 2) Histogram — Severity Distribution
# ----------------------------
st.subheader("2) Accident Severity Distribution")
st.write("Question: How are accident severities distributed?")

fig_hist = px.histogram(
    filtered_df,
    x='Severity',
    nbins=len(severity_values),
    labels={'Severity':'Severity Level'},
    title='Severity Distribution of Accidents',
    color='Severity',
)
st.plotly_chart(fig_hist, use_container_width=True)

with st.expander("How to read this chart"):
    st.write("""
    - X axis: Severity level (1–4)  
    - Y axis: Number of accidents  
    - Each bar represents the count of accidents for that severity  
    - Filter selections in the sidebar affect this chart
    """)

st.markdown("**Observations:**")
st.write("""
- Most accidents are lower severity (1–2) in the sample.  
- Filtering by states and severity changes the distribution.  
- Helps understand overall accident severity trends.
""")

st.markdown("---")

# ----------------------------
# 3) Scatter Plot — Visibility vs Temperature
# ----------------------------
st.subheader("3) Visibility vs Temperature")
st.write("Question: Is visibility related to temperature?")

scatter_df = filtered_df.dropna(subset=['Visibility(mi)','Temperature(F)']).sample(n=min(2000,len(filtered_df)))

fig_scatter = px.scatter(
    scatter_df,
    x='Temperature(F)',
    y='Visibility(mi)',
    color='Severity',
    hover_data=['Start_Time','State','City','Temperature(F)','Visibility(mi)','Severity'],
    title='Visibility vs Temperature by Severity',
    labels={'Temperature(F)':'Temperature (°F)','Visibility(mi)':'Visibility (mi)'}
)

st.plotly_chart(fig_scatter, use_container_width=True)

with st.expander("How to read this chart"):
    st.write("""
    - Each dot represents an accident (sampled for performance)  
    - X axis: temperature in Fahrenheit  
    - Y axis: visibility in miles  
    - Color indicates severity  
    - Hover over points for date, city, temperature, visibility, and severity
    """)

st.markdown("**Observations:**")
st.write("""
- Most points cluster around common visibility values (~10 mi)  
- No strong linear correlation between temperature and visibility is visible  
- Color helps distinguish severity trends visually
""")

st.markdown("---")

# ----------------------------
# 4) Map — Accidents by Location
# ----------------------------
st.subheader("4) Map of Accidents")
st.write("Question: Where do most accidents occur geographically?")

# Aggregate by city or coordinates
map_df = filtered_df.groupby(['City','State','Latitude','Longitude']).size().reset_index(name='Accidents')

fig_map = px.scatter_mapbox(
    map_df,
    lat='Latitude',
    lon='Longitude',
    size='Accidents',
    color='Accidents',
    color_continuous_scale=px.colors.sequential.OrRd,
    size_max=25,
    hover_name='City',
    hover_data=['State','Accidents'],
    zoom=3,
    title='Accidents by Location'
)

fig_map.update_layout(mapbox_style="open-street-map")
fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig_map, use_container_width=True)

with st.expander("How to read this chart"):
    st.write("""
    - Each circle represents a city/location  
    - Circle size and color intensity indicate the number of accidents  
    - Hover to see city, state, and exact accident count  
    - Darker / bigger circles → more accidents
    """)

st.markdown("**Observations:**")
st.write("""
- High-accident cities are immediately visible by larger, darker circles  
- Geographic patterns can reveal clusters or hotspots  
- Useful for understanding accident distribution across regions
""")

