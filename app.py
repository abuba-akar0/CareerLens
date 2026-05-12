import streamlit as st
from ui_components import load_custom_css

st.set_page_config(page_title="CareerLens Pakistan", page_icon="🎓", layout="wide")
load_custom_css()

def show_home():
    st.markdown('<div style="text-align:center;padding:40px 0 20px 0;"><span style="font-size:4.5rem;">🎓</span></div>', unsafe_allow_html=True)
    st.markdown('<h1 style="text-align:center; font-size: 3.5rem; margin-bottom: 0;">Welcome to CareerLens</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; font-size: 1.2rem; color: #8888aa; margin-bottom: 30px;">AI Guidance for Pakistani Students & Professionals</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Start Your AI Career Match", use_container_width=True, type="primary"):
            st.switch_page("pages/ai_matcher.py")
            
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown('<div class="metric-box"><div class="metric-val">74+</div><div class="metric-label">Local Careers</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="metric-box"><div class="metric-val">Smart</div><div class="metric-label">AI Matching Engine</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="metric-box"><div class="metric-val">Verified</div><div class="metric-label">Market Salary Data</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🛠️ Platform Features")
    
    f1, f2 = st.columns(2)
    with f1:
        with st.container(border=True):
            st.markdown("#### 🎯 AI Matcher")
            st.markdown("<p style='color:#c8c8d4; font-size:0.95rem;'>Take our advanced compass quiz or simply describe your interests. Our AI will map your query against the Pakistani job market.</p>", unsafe_allow_html=True)
            if st.button("Launch Matcher", key="home_matcher"): st.switch_page("pages/ai_matcher.py")
            
        with st.container(border=True):
            st.markdown("#### 📚 Career Directory")
            st.markdown("<p style='color:#c8c8d4; font-size:0.95rem;'>Browse and search our comprehensive database of 74+ careers, including modern fields like Aerospace and Web3.</p>", unsafe_allow_html=True)
            if st.button("Open Directory", key="home_dir"): st.switch_page("pages/directory.py")
            
    with f2:
        with st.container(border=True):
            st.markdown("#### 📊 Readiness Assessment")
            st.markdown("<p style='color:#c8c8d4; font-size:0.95rem;'>Rate yourself on 5 key metrics. Our linear regression model will instantly calculate your professional readiness score.</p>", unsafe_allow_html=True)
            if st.button("Check Readiness", key="home_ready"): st.switch_page("pages/readiness.py")
            
        with st.container(border=True):
            st.markdown("#### ⚖️ Compare Careers")
            st.markdown("<p style='color:#c8c8d4; font-size:0.95rem;'>Put two careers side-by-side to compare their salary ranges (Min/Avg/Max) and educational roadmaps.</p>", unsafe_allow_html=True)
            if st.button("Compare Now", key="home_comp"): st.switch_page("pages/compare.py")

# Define Pages
home_page = st.Page(show_home, title="Home", icon="🏠", default=True)
matcher_page = st.Page("pages/ai_matcher.py", title="AI Matcher", icon="🎯")
readiness_page = st.Page("pages/readiness.py", title="Readiness Assessment", icon="📊")
directory_page = st.Page("pages/directory.py", title="Career Directory", icon="📚")
compare_page = st.Page("pages/compare.py", title="Compare Careers", icon="⚖️")

# Initialize Navigation
pg = st.navigation([home_page, matcher_page, readiness_page, directory_page, compare_page])

# Shared Sidebar Elements
st.sidebar.markdown('<div style="text-align:center;padding:20px 0;"><span style="font-size:3rem;">🎓</span></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="text-align:center;"><span style="font-size:1.5rem;font-weight:800;background:linear-gradient(135deg,#667eea,#764ba2);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">CareerLens</span><br><span style="font-size:0.85rem;color:#8888aa;">AI Guidance for Pakistan</span></div>', unsafe_allow_html=True)
st.sidebar.markdown("---")

# Run the selected page
pg.run()