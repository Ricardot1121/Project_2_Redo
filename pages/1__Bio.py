import streamlit as st
from pathlib import Path
 
st.title("My Bio")
 
# ---------- TODO: Replace with your own info ----------
NAME = "Ricardo Torres"
PROGRAM = "Computer Science / Data Visualization / Game Development"

# Professional Summary
PROFESSIONAL_SUMMARY = """
I am a passionate Computer Science student specializing in Data Visualization and Game Development. 
With a strong foundation in programming and an eye for interactive design, I bridge the gap between 
complex data analysis and engaging user experiences. My work focuses on creating intuitive, 
accessible visualizations that help people understand and explore data effectively.
"""

# Key Highlights
HIGHLIGHTS = [
    "🎓 Computer Science student with focus on Data Visualization",
    "💻 Proficient in Python, Streamlit, and interactive dashboard development",
    "📊 Experience with data analysis libraries (Pandas, Plotly, NumPy)",
    "🎮 Game development background bringing creativity to data storytelling",
    "🌐 Committed to accessible and user-friendly design principles"
]

# Visualization Philosophy
VIZ_PHILOSOPHY = """
**My Data Visualization Philosophy:**

I believe that great data visualization is about more than just pretty charts—it's about telling 
compelling stories that drive understanding and action. My approach emphasizes:

- **Clarity First**: Every visualization should answer a specific question clearly
- **Accessibility**: Designs must be inclusive and usable by everyone
- **Interactivity**: Users should be able to explore data at their own pace
- **Context Matters**: Data without context is just numbers; context transforms it into insight
- **Ethical Responsibility**: Always acknowledge data limitations and avoid misleading representations
"""

FUN_FACTS = [
    "🥾 Love hiking and outdoor adventures - nature inspires my color palette choices",
    "🎮 Game development background helps me think about user engagement in dashboards",
    "📚 Currently exploring advanced statistical visualization techniques",
    "🌟 Passionate about making data accessible to non-technical audiences"
]

def find_photo(filename="My_Profile_Pic.jpg"):
    # Photo was saved in assets folder
    try:
        script_dir = Path(__file__).resolve().parent
    except NameError:
        script_dir = Path.cwd()
 
    candidates = [
        script_dir / "assets" / filename,          # pages/assets/...
        script_dir.parent / "assets" / filename,   # root/assets/... (common)
        Path("assets") / filename,                 # cwd/assets/...
    ]
    for p in candidates:
        if p.exists():
            return str(p)
    return None
 
photo_src = find_photo("My_Profile_Pic.jpg")
 
# -------------------- LAYOUT --------------------
# Header Section
col1, col2 = st.columns([1, 2], vertical_alignment="center")
 
with col1:
    if photo_src:
        # Image with proper alt-text for accessibility
        st.image(
            photo_src, 
            caption=NAME, 
            use_container_width=True,
            # Alt-text for screen readers
        )
        st.caption("Professional headshot of Ricardo Torres, Computer Science student specializing in data visualization")
    else:
        st.info(
            "📷 Place `My_Profile_Pic.jpg` inside an `assets/` folder at the app root "
            "or update the path in `find_photo()`."
        )

with col2:
    st.subheader(f"👋 Hello, I'm {NAME}")
    st.write(f"**{PROGRAM}**")
    
    # Professional Summary
    st.markdown("### 📋 Professional Summary")
    st.write(PROFESSIONAL_SUMMARY)

st.divider()

# Key Highlights Section
st.markdown("### ⭐ Key Highlights")
for highlight in HIGHLIGHTS:
    st.write(highlight)

st.divider()

# Visualization Philosophy Section
st.markdown("### 🎨 Data Visualization Philosophy")
st.markdown(VIZ_PHILOSOPHY)

st.divider()

# Fun Facts Section
st.markdown("### 🎯 Fun Facts About Me")
for fact in FUN_FACTS:
    st.write(fact)

st.divider()

# Footer
st.markdown("### 📬 Connect With Me")
st.write("""
Feel free to explore my work through this portfolio app! Each section demonstrates different aspects 
of my data visualization skills, from exploratory data analysis to interactive dashboards.
""")

st.caption("💡 This bio page showcases professional summary, highlights, visualization philosophy, and personal interests as required for the portfolio project.")
