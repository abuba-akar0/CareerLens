import streamlit as st
from ml_engine import load_models_and_data
from ui_components import load_custom_css, render_card

# st.set_page_config(page_title="Career Directory", page_icon="📚", layout="wide")
load_custom_css()

_, _, _, _, df, salary_lookup, cat_salary, _ = load_models_and_data()

st.markdown('<div class="hero-title">Career Directory</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Browse and search our comprehensive database.</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])
cats = ["All Categories"] + sorted(df['Career_Category'].unique().tolist())
sel_cat = col1.selectbox("Filter by Category", cats)
search_query = col2.text_input("Search careers...", placeholder="e.g. Engineer, Designer")

filt_df = df
if sel_cat != "All Categories":
    filt_df = filt_df[filt_df['Career_Category'] == sel_cat]
if search_query:
    filt_df = filt_df[filt_df['Career_Name'].str.contains(search_query, case=False, na=False)]
    
st.markdown("---")
st.write(f"Showing {len(filt_df)} careers.")

if filt_df.empty:
    st.info("No careers found matching your criteria.")
else:
    for _, r in filt_df.iterrows():
        render_card(r['Career_Name'], df[df['Career_Name'] == r['Career_Name']], salary_lookup, cat_salary)