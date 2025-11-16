import streamlit as st
from datetime import datetime

# -----------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------
st.set_page_config(
    page_title="Data Portfolio – Your Name",
    page_icon="📊",
    layout="wide"
)

# -----------------------------------------------------------
# Branding / Header
# -----------------------------------------------------------
st.title("📊 Data Science & Visualization Portfolio")
st.subheader("By **Your Name**")
st.caption("A multi-page analytics app featuring a professional bio, EDA gallery, dashboard, and future work.")

# -----------------------------------------------------------
# Main Description
# -----------------------------------------------------------
st.markdown(
    """
    Welcome! This portfolio app includes:
    
    ### 🧑‍💼 Bio  
    A short professional introduction, highlights, and visualization philosophy.

    ### 📊 EDA Gallery  
    Four exploratory visualizations with descriptions, explanations, and insights.

    ### 📈 Dashboard  
    Interactive filters, KPIs, linked charts, and narrative interpretation.

    ### 🧭 Future Work  
    Next steps, reflections, and improvements.

    Use the **sidebar** to navigate between pages.
    """
)

# -----------------------------------------------------------
# Optional: App Organization Expander
# -----------------------------------------------------------
with st.expander("ℹ️ How this App is Organized"):
    st.write(
        """
        - `app.py` → Main entry page  
        - `pages/1_📄_Bio.py` → Bio page  
        - `pages/2_📊_Charts_Gallery.py` → EDA gallery  
        - `pages/3_📈_Dashboard.py` → Main dashboard  
        - `pages/4_🧭_Future_Work.py` → Future improvements & reflection  

        Add CSVs (under 25MB) into `/data/`.
        Images, icons, and logos go in `/assets/`.
        """
    )

# -----------------------------------------------------------
# Footer
# -----------------------------------------------------------
st.markdown("---")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d')} • Built with Streamlit 🌱")
