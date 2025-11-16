# pages/3_Dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# -----------------------------------------------------------
# Page Title
# -----------------------------------------------------------
st.title("📈 Dashboard — USA Accidents Overview")

# -----------------------------------------------------------
# Load Data
# -----------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/accidents_small.csv")
    df['Start_Time'] = pd.to_datetime(df['Start_Time'], errors='coerce')
    return df

df = load_data()
st.write(f"Dataset rows: {len(df)}")

# -----------------------------------------------------------
# Filters
# -----------------------------------------------------------
st.sidebar.header("Dashboard Filters")

# States
states = sorted(df['State'].dropna().unique())
selected_states = st.sidebar.multiselect("Select States", states, default=states[:5])

# Temperature range filter
temp_min = float(df['Temperature(F)'].min()) if not df['Temperature(F)'].isna().all() else 0
temp_max = float(df['Temperature(F)'].max()) if not df['Temperature(F)'].isna().all() else 100
selected_temp_range = st.sidebar.slider("Temperature Range (°F)", temp_min, temp_max, (temp_min, temp_max))

# Date range with error handling
try:
    valid_dates = df['Start_Time'].dropna()
    if len(valid_dates) > 0:
        min_date = valid_dates.min().date()
        max_date = valid_dates.max().date()
        selected_dates = st.sidebar.date_input(
            "Select Date Range",
            value=[min_date, max_date],
            min_value=min_date,
            max_value=max_date
        )
    else:
        st.sidebar.warning("No valid dates found")
        selected_dates = []
except Exception as e:
    st.sidebar.error(f"Date processing error: {str(e)}")
    selected_dates = []

# Guard against empty selection
if isinstance(selected_dates, list) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
else:
    start_date, end_date = min_date, max_date

# Filtered dataframe
if len(selected_dates) == 2:
    start_date, end_date = selected_dates
    filtered_df = df[
        (df['State'].isin(selected_states)) &
        (df['Temperature(F)'].between(selected_temp_range[0], selected_temp_range[1])) &
        (df['Start_Time'].dt.date.between(start_date, end_date))
    ]
else:
    filtered_df = df[
        (df['State'].isin(selected_states)) &
        (df['Temperature(F)'].between(selected_temp_range[0], selected_temp_range[1]))
    ]

# -----------------------------------------------------------
# KPIs
# -----------------------------------------------------------
st.subheader("Key Performance Indicators (KPIs)")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric("Total Accidents", len(filtered_df))
kpi2.metric("Avg Temperature", f"{round(filtered_df['Temperature(F)'].mean(), 1)}°F" if not filtered_df.empty else "N/A")
kpi3.metric("Unique States", filtered_df['State'].nunique())
kpi4.metric("Latest Accident", filtered_df['Start_Time'].max().strftime("%Y-%m-%d") if not filtered_df.empty and not filtered_df['Start_Time'].isna().all() else "N/A")

st.markdown("---")

# -----------------------------------------------------------
# Charts
# -----------------------------------------------------------
st.subheader("Linked Charts")

# 1) Accidents by State (Bar)
if not filtered_df.empty:
    state_counts = filtered_df['State'].value_counts().reset_index()
    state_counts.columns = ['State', 'Count']
    fig_state = px.bar(
        state_counts,
        x='State', y='Count',
        title="Accidents by State",
        text='Count'
    )
    st.plotly_chart(fig_state, use_container_width=True)

    # 2) Temperature over Time (Line)
    temp_time = filtered_df.dropna(subset=['Start_Time', 'Temperature(F)']).copy()
    if len(temp_time) > 0:
        temp_time['Date'] = temp_time['Start_Time'].dt.date
        daily_temp = temp_time.groupby('Date')['Temperature(F)'].mean().reset_index()
        daily_temp['Date'] = pd.to_datetime(daily_temp['Date'])
        fig_line = px.line(
            daily_temp,
            x='Date', y='Temperature(F)',
            title="Average Temperature Over Time"
        )
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("No valid temperature data for selected filters.")
else:
    st.warning("No data available for the selected filters.")

st.markdown("---")

# -----------------------------------------------------------
# Narrative / Insights
# -----------------------------------------------------------
st.subheader("Narrative Insights")
st.write("""
- **Accident hotspots:** The bar chart shows which states have the most accidents in the selected filters.  
- **Trends over time:** The line chart shows how average temperatures vary across time. This may indicate seasonal patterns.  
- **Filter impact:** Adjusting the state, temperature, or date filters will update both charts and KPIs instantly.  
- **Data coverage:** Some states may have fewer reported accidents due to underreporting or data limitations.  
""")

# -----------------------------------------------------------
# Footer
# -----------------------------------------------------------
st.markdown("---")
st.caption(f"Data source: Kaggle — USA Accidents Dataset | Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
