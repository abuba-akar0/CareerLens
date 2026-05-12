import streamlit as st
from ml_engine import get_salary

def load_custom_css():
    st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .main { background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 50%, #24243e 100%); color: #fff; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #1a1a3e 0%, #0f0c29 100%); border-right: 1px solid rgba(255,255,255,0.05); }
    [data-testid="stSidebar"] * { color: #e0e0e0 !important; }
    h1, h2, h3, h4, h5 { color: #ffffff !important; }
    p, li, .stMarkdown { color: #f3f4f6 !important; line-height: 1.6; }
    label { color: #ffffff !important; font-weight: 600 !important; }
    .stButton>button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 8px; padding: 10px 24px; font-weight: 600; border: none; transition: all 0.3s ease; width: 100%; font-size: 1rem; letter-spacing: 0.5px; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(102,126,234,0.4); }
    .career-card { background: rgba(255,255,255,0.02); backdrop-filter: blur(15px); padding: 24px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05); margin-bottom: 20px; transition: all 0.3s ease; }
    .career-card:hover { border-color: rgba(102,126,234,0.5); box-shadow: 0 8px 25px rgba(102,126,234,0.2); }
    .career-title { color: #fff !important; font-size: 1.5rem; font-weight: 700; margin-bottom: 5px; }
    .category-tag { background: rgba(102,126,234,0.1); color: #667eea !important; padding: 6px 14px; border-radius: 20px; font-weight: 600; display: inline-block; margin: 5px 0; font-size: 0.85rem; border: 1px solid rgba(102,126,234,0.2); }
    .hero-title { font-size: 2.8rem; font-weight: 800; background: linear-gradient(135deg, #667eea, #764ba2, #f093fb); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 5px; line-height: 1.2; }
    .hero-sub { color: #8888aa !important; font-size: 1.1rem; margin-bottom: 25px; }
    .stTextArea textarea, .stSelectbox > div > div { background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.1) !important; color: #e0e0e0 !important; border-radius: 10px !important; }
    .timeline-item { border-left: 2px solid #667eea; padding-left: 15px; margin-bottom: 15px; position: relative; }
    .timeline-item::before { content: ''; position: absolute; left: -6px; top: 5px; width: 10px; height: 10px; border-radius: 50%; background: #f093fb; }
    </style>""", unsafe_allow_html=True)

def format_currency(amount):
    return f"Rs. {amount:,}"

def render_card(name, row, salary_lookup, cat_salary, rank=None, score=None):
    cat = row['Career_Category'].values[0]
    sal = get_salary(name, cat, salary_lookup, cat_salary)
    desc = row['Description'].values[0]
    
    rank_html = f'<span style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 4px 10px; border-radius: 5px; font-weight: bold; margin-right: 10px;">#{rank}</span>' if rank else ''
    match_html = f'<span style="float:right; color:#f093fb; font-weight:600;">{score*100:.0f}% Match</span>' if score is not None else ''
    
    st.markdown(f"""
    <div class="career-card">
        <div style="margin-bottom: 10px;">
            {rank_html}<span class="career-title">{name}</span>{match_html}
        </div>
        <div style="margin-bottom: 15px;">
            <span class="category-tag">📂 {cat}</span>
        </div>
        <p style="color: #f3f4f6; font-size: 0.95rem; line-height: 1.6;">{desc}</p>
        <div style="background: rgba(46,213,115,0.05); border: 1px solid rgba(46,213,115,0.2); padding: 12px; border-radius: 8px; margin-top: 15px;">
            <div style="color: #2ed573; font-weight: 600; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 5px;">Salary Expectations (PKR/mo)</div>
            <div style="display: flex; justify-content: space-between;">
                <div><span style="color:#8888aa; font-size:0.8rem;">Min:</span> <br><b>{format_currency(sal['min'])}</b></div>
                <div><span style="color:#8888aa; font-size:0.8rem;">Avg:</span> <br><b>{format_currency(sal['avg'])}</b></div>
                <div><span style="color:#8888aa; font-size:0.8rem;">Max:</span> <br><b>{format_currency(sal['max'])}</b></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📌 Roadmap, Education & Universities"):
        t1, t2, t3 = st.tabs(["📌 Roadmap", "🎓 Education", "🏫 Universities"])
        
        with t1:
            steps = str(row['Roadmap'].values[0]).split(' | ')
            for i, step in enumerate(steps):
                clean_step = step.strip().replace(f'Step {i+1}: ', '').replace(f'Step {i+1} ', '')
                if clean_step:
                    st.markdown(f'<div class="timeline-item"><b>Phase {i+1}</b><br><span style="color:#f3f4f6; font-size:0.9rem;">{clean_step}</span></div>', unsafe_allow_html=True)
        with t2:
            st.markdown(f"**Intermediate Path:** {row['Intermediate_Path'].values[0]}")
            st.markdown(f"**Required Degree:** {row['Required_Degree'].values[0]}")
        with t3:
            provinces = {"Punjab": 'Universities_Punjab', "Sindh": 'Universities_Sindh', "KPK": 'Universities_KPK', "Balochistan": 'Universities_Balochistan', "Islamabad": 'Universities_Islamabad'}
            for prov, col in provinces.items():
                if col in row.columns:
                    unis = str(row[col].values[0]).split(';')
                    if unis and unis[0].strip() and unis[0].strip() != "Not specified":
                        st.markdown(f"**{prov}:**")
                        tags = "".join([f'<span style="background: rgba(255,255,255,0.05); padding: 4px 10px; border-radius: 15px; font-size: 0.8rem; margin: 0 5px 5px 0; display: inline-block;">{u.strip()}</span>' for u in unis])
                        st.markdown(tags, unsafe_allow_html=True)