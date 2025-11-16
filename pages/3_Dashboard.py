# 3_📈_Dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Dashboard", page_icon="📈", layout="wide")

st.title("📈 Dashboard — USA Accidents Overview")

# ----------------------------
# Load Data
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_parquet("data/accidents_small.parquet")
    df['Start_Time'] = pd.to_datetime(df['Start_Time'])
    return df

df = load_data()
st.write(f"Dataset rows: {len(df)}")

# ----------------------------
# Filters
# ----------------------------
st.sidebar.header("Dashboard Filters")

# States
states = sorted(df['State'].dropna().unique())
selected_states = st.sidebar.multiselect("Select States", states, default=states[:5])

# Severity
severity_values = sorted(df['Severity'].dropna().unique())
selected_severity = st.sidebar.multiselect("Select Severity", severity_values, default=severity_values)

# Date range
min_date = df['Start_Time'].min().date()
max_date = df['Start_Time'].max().date()
selected_dates = st.sidebar.date_input(
    "Select Date Range",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Filtered dataframe
filtered_df = df[
    (df['State'].isin(selected_states)) &
    (df['Severity'].isin(selected_severity)) &
    (df['Start_Time'].dt.date.between(selected_dates[0], selected_dates[1]))
]

# ----------------------------
# KPIs
# ----------------------------
st.subheader("Key Performance Indicators (KPIs)")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric("Total Accidents", len(filtered_df))
kpi2.metric("Average Severity", round(filtered_df['Severity'].mean(),2))
kpi3.metric("Unique States", filtered_df['State'].nunique())
kpi4.metric("Latest Accident", filtered_df['Start_Time'].max().strftime("%Y-%m-%d"))

st.markdown("---")

# ----------------------------
# Charts
# ----------------------------
st.subheader("Linked Charts")

# 1) Accidents by State (Bar)
state_counts = filtered_df['State'].value_counts().reset_index()
state_counts.columns = ['State','Count']
fig_state = px.bar(
    state_counts,
    x='State', y='Count',
    title="Accidents by State",
    text='Count'
)
st.plotly_chart(fig_state, use_container_width=True)

# 2) Severity over Time (Line)
severity_time = filtered_df.groupby([filtered_df['Start_Time'].dt.date, 'Severity']).size().reset_index(name='Count')
fig_line = px.line(
    severity_time,
    x='Start_Time', y='Count', color='Severity',
    title="Accident Severity Over Time"
)
st.plotly_chart(fig_line, use_container_width=True)

st.markdown("---")

# ----------------------------
# Narrative / Insights
# ----------------------------
st.subheader("Narrative Insights")
st.write("""
- **Accident hotspots:** The bar chart shows which states have the most accidents in the selected filters.  
- **Trends over time:** The line chart shows how severity levels vary across time. Peaks may indicate seasonal effects or reporting patterns.  
- **Filter impact:** Adjusting the state, severity, or date filters will update both charts and KPIs instantly.  
- **Data coverage:** Some states may have fewer reported accidents due to underreporting or data limitations.  
""")

# ----------------------------
# Footer: Data source & last refreshed
# ----------------------------
st.markdown("---")
st.caption(f"Data source: Kaggle — USA Accidents Dataset | Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
