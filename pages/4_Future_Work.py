# 4_🧭_Future_Work.py
import streamlit as st

st.set_page_config(page_title="Future Work", page_icon="🧭")

st.title("🧭 Future Work & Reflection")

# ----------------------------
# Next Steps / Improvements
# ----------------------------
st.subheader("Next Steps / Improvements")
st.write("""
Here are some concrete next steps I would pursue to enhance this portfolio and dashboard:

- **Forecasting & trend analysis:** Add predictive models to estimate accident counts by state or severity.  
- **Additional filters & KPIs:** Include weather conditions, time of day, or road type to explore correlations.  
- **Enhanced geospatial analysis:** Use clustering or heatmaps to identify high-risk zones more precisely.  
- **Accessibility improvements:** Add color-blind safe palettes, alternative text for charts, and keyboard navigation support.  
- **Data enrichment:** Integrate external datasets (traffic volume, population, or demographics) to provide context.
""")

st.markdown("---")

# ----------------------------
# Reflection on Prototype → Final Build
# ----------------------------
st.subheader("Reflection")
st.write("""
- The final app is multi-page, fully interactive, and uses real dataset visualizations, unlike the initial static prototype.  
- Charts now include hover tooltips, linked filters, and KPIs for dynamic exploration.  
- The map visualization was added to enhance geospatial insights, which was not in the prototype.  
- Sidebar filters improve user navigation and exploration, making the dashboard more usable and informative.
""")

st.markdown("---")

# ----------------------------
# Accessibility & Ethics Reminder
# ----------------------------
st.subheader("Accessibility & Ethics Notes")
st.write("""
- Color palettes were chosen to be color-blind friendly and charts include clear labels.  
- The dataset contains real people involved in accidents; visualizations reflect patterns only, not individual behaviors.  
- Interpret results carefully; reporting may be biased by underreporting or regional differences.
""")

st.caption("End of Future Work Page — Built with Streamlit 🌱")

