import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json

st.set_page_config(page_title="CareerLens Pakistan", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

# --- Premium CSS ---
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
.main { background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 50%, #24243e 100%); }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #1a1a3e 0%, #0f0c29 100%); border-right: 1px solid rgba(255,255,255,0.05); }
[data-testid="stSidebar"] * { color: #e0e0e0 !important; }
h1, h2, h3 { color: #ffffff !important; }
p, li, label, .stMarkdown { color: #c8c8d4 !important; }
.stButton>button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 12px; padding: 12px 28px; font-weight: 600; border: none; transition: all 0.4s ease; width: 100%; font-size: 1.05rem; letter-spacing: 0.5px; }
.stButton>button:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(102,126,234,0.4); }
.career-card { background: rgba(255,255,255,0.04); backdrop-filter: blur(12px); padding: 28px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.08); margin-bottom: 24px; transition: all 0.3s ease; }
.career-card:hover { border-color: rgba(102,126,234,0.4); box-shadow: 0 8px 32px rgba(102,126,234,0.15); }
.career-title { color: #fff !important; font-size: 1.6rem; font-weight: 700; margin-bottom: 8px; }
.salary-tag { background: linear-gradient(135deg, rgba(46,213,115,0.15), rgba(46,213,115,0.05)); color: #2ed573 !important; padding: 8px 16px; border-radius: 25px; font-weight: 600; display: inline-block; margin: 8px 8px 8px 0; font-size: 0.85rem; border: 1px solid rgba(46,213,115,0.2); }
.category-tag { background: linear-gradient(135deg, rgba(102,126,234,0.15), rgba(102,126,234,0.05)); color: #667eea !important; padding: 8px 16px; border-radius: 25px; font-weight: 600; display: inline-block; margin: 8px 0; font-size: 0.85rem; border: 1px solid rgba(102,126,234,0.2); }
.hero-title { font-size: 3rem; font-weight: 800; background: linear-gradient(135deg, #667eea, #764ba2, #f093fb); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 8px; line-height: 1.2; }
.hero-sub { color: #8888aa !important; font-size: 1.15rem; margin-bottom: 32px; }
.metric-box { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; text-align: center; }
.metric-val { font-size: 2rem; font-weight: 800; color: #667eea !important; }
.metric-label { font-size: 0.8rem; color: #8888aa !important; text-transform: uppercase; letter-spacing: 1px; }
.match-rank { background: linear-gradient(135deg, #667eea, #764ba2); color: white !important; width: 36px; height: 36px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-weight: 700; font-size: 1rem; margin-right: 12px; }
.readiness-bar { height: 10px; border-radius: 5px; background: rgba(255,255,255,0.08); overflow: hidden; margin: 8px 0; }
.readiness-fill { height: 100%; border-radius: 5px; transition: width 0.8s ease; }
.stTextArea textarea { background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,255,255,0.1) !important; color: #e0e0e0 !important; border-radius: 12px !important; }
.stSelectbox > div > div { background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,255,255,0.1) !important; color: #e0e0e0 !important; border-radius: 12px !important; }
.stExpander { background: rgba(255,255,255,0.02) !important; border: 1px solid rgba(255,255,255,0.06) !important; border-radius: 12px !important; }
.compare-header { background: linear-gradient(135deg, rgba(102,126,234,0.1), rgba(118,75,162,0.1)); border: 1px solid rgba(102,126,234,0.2); border-radius: 12px; padding: 16px; margin-bottom: 16px; text-align: center; }
</style>""", unsafe_allow_html=True)


# --- Load Models & Data ---
@st.cache_resource(show_spinner="Loading AI Models...")
def load_models():
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    knn = joblib.load('models/knn_model.pkl')
    le = joblib.load('models/le_career.pkl')
    try:
        readiness = joblib.load('models/readiness_model.pkl')
    except:
        readiness = None
    return embedder, knn, le, readiness

@st.cache_data
def load_data():
    df = pd.read_csv('data/careers_pakistan.csv')
    df.fillna("Not specified", inplace=True)
    
    with open('models/salary_lookup.json') as f:
        sal = json.load(f)
    with open('models/category_salary_fallback.json') as f:
        cat_sal = json.load(f)
        
    # Pre-compute semantic content for matching
    # Combining name, keywords, and description for a rich search space
    df['search_content'] = df['Career_Name'] + " " + df['Career_Category'] + " " + df['Keywords'] + " " + df['Description']
    
    return df, sal, cat_sal

@st.cache_resource
def get_career_embeddings(_df, _embedder):
    """Compute and cache embeddings for all careers in the dataset."""
    return _embedder.encode(_df['search_content'].tolist())

# Load resources
try:
    embedder, knn_model, le_career, readiness_model = load_models()
    df, salary_lookup, cat_salary = load_data()
    # Compute career embeddings once
    all_career_embs = get_career_embeddings(df, embedder)
except Exception as e:
    st.error(f"Error loading resources: {e}")
    st.stop()


# --- Helpers ---
def fmt(amount):
    return f"{amount/100000:.1f}L" if amount >= 100000 else f"{amount/1000:.0f}K"

def get_salary(name, cat):
    s = salary_lookup.get(name)
    if not s:
        s = cat_salary.get(cat, {"min": 0, "max": 0, "avg": 0})
    return s

def get_readiness(embedding, career_name):
    """Try to get readiness prediction for a career match."""
    if readiness_model is None:
        return None
    try:
        result = readiness_model.predict(embedding)
        return result[0]
    except:
        try:
            result = readiness_model.predict_proba(embedding)
            return result[0]
        except:
            return None

def render_card(name, row, rank=None, score=None, readiness_val=None):
    cat = row['Career_Category'].values[0]
    sal = get_salary(name, cat)
    desc = row['Description'].values[0]
    
    # Building the header part in one markdown call to avoid layout breaks
    rank_html = f'<span class="match-rank">#{rank}</span>' if rank else ''
    conf_html = f'<span style="float:right;color:#667eea;font-weight:600;">{score*100:.0f}% match</span>' if score and score <= 1 else ''
    
    header_html = f"""
    <div class="career-card">
        {rank_html}<span class="career-title">{name}</span>{conf_html}
        <div style="margin-top: 10px;">
            <span class="salary-tag">💰 PKR {fmt(sal["min"])} – {fmt(sal["max"])}/mo</span>
            <span class="category-tag">📂 {cat}</span>
        </div>
        <p style="margin-top: 15px; color: #c8c8d4; font-style: italic;">{desc}</p>
    """
    
    # Readiness display inside the card div if applicable
    readiness_html = ""
    if readiness_val is not None:
        if isinstance(readiness_val, (int, float, np.integer, np.floating)):
            pct = min(max(float(readiness_val), 0), 100)
            color = "#2ed573" if pct >= 70 else "#ffa502" if pct >= 40 else "#ff4757"
            readiness_html = f"""
            <div style="margin-top: 20px;">
                <strong style="color:white;">🎯 Readiness Score: {pct:.0f}%</strong>
                <div class="readiness-bar"><div class="readiness-fill" style="width:{pct}%;background:{color};"></div></div>
            </div>
            """
        else:
            readiness_html = f'<div style="margin-top: 20px;"><strong style="color:white;">🎯 Readiness Level:</strong> <code style="color:#f093fb;">{readiness_val}</code></div>'
    
    st.markdown(header_html + readiness_html + "</div>", unsafe_allow_html=True)
    
    # Use a container for the interactive parts
    with st.container():
        # Salary Chart
        with st.expander("💰 Salary Breakdown"):
            chart_df = pd.DataFrame({"Range": ["Minimum", "Average", "Maximum"],
                                     "PKR": [sal.get("min",0), sal.get("avg", (sal.get("min",0)+sal.get("max",0))//2), sal.get("max",0)]})
            st.bar_chart(chart_df.set_index("Range"), color="#667eea")
        
        # Roadmap
        with st.expander("📌 Roadmap to Success", expanded=(rank==1 if rank else False)):
            steps = str(row['Roadmap'].values[0]).split(' | ')
            for i, step in enumerate(steps):
                st.markdown(f"**Step {i+1}.** {step.strip().replace('Step ' + str(i+1) + ': ', '').replace('Step ' + str(i+1) + ' ', '')}")
        
        # Education
        with st.expander("🎓 Education"):
            c1, c2 = st.columns(2)
            c1.metric("Intermediate", row['Intermediate_Path'].values[0])
            c2.metric("Degree", str(row['Required_Degree'].values[0])[:50] + ("..." if len(str(row['Required_Degree'].values[0])) > 50 else ""))
        
        # Universities
        with st.expander("🏫 Universities by Province"):
            provinces = {"Punjab": 'Universities_Punjab', "Sindh": 'Universities_Sindh',
                         "KPK": 'Universities_KPK', "Balochistan": 'Universities_Balochistan', "Islamabad": 'Universities_Islamabad'}
            tabs = st.tabs(list(provinces.keys()))
            for tab, (prov, col) in zip(tabs, provinces.items()):
                unis = str(row[col].values[0]).split(';')
                for u in unis:
                    tab.markdown(f"• {u.strip()}")



# --- Sidebar ---
st.sidebar.markdown('<div style="text-align:center;padding:20px 0;"><span style="font-size:2.5rem;">🎓</span></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="text-align:center;"><span style="font-size:1.4rem;font-weight:700;background:linear-gradient(135deg,#667eea,#764ba2);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">CareerLens</span><br><span style="font-size:0.8rem;color:#666;">AI Career Guidance for Pakistan</span></div>', unsafe_allow_html=True)
st.sidebar.markdown("---")
page = st.sidebar.radio("", ["🎯 AI Career Matcher", "📚 Career Directory", "⚖️ Compare Careers", "ℹ️ About"])
st.sidebar.markdown("---")

# Stats in sidebar
st.sidebar.markdown(f"""
<div class="metric-box"><div class="metric-val">{len(df)}</div><div class="metric-label">Careers</div></div>
""", unsafe_allow_html=True)
st.sidebar.markdown("")
st.sidebar.markdown(f"""
<div class="metric-box"><div class="metric-val">{df['Career_Category'].nunique()}</div><div class="metric-label">Categories</div></div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.caption("💡 Be descriptive in the AI Matcher for best results.")


# ====== PAGE: AI CAREER MATCHER ======
if page == "🎯 AI Career Matcher":
    st.markdown('<div class="hero-title">Find Your Dream Career</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Describe your interests, skills and passions — our AI will match you with the best careers in Pakistan.</div>', unsafe_allow_html=True)
    
    user_input = st.text_area("Tell us about yourself...",
        placeholder="e.g., I enjoy solving math problems, building things with code, and I'm fascinated by artificial intelligence...",
        height=140, label_visibility="collapsed")
    
    if st.button("Find My Career Match 🚀"):
        if len(user_input.split()) < 3:
            st.warning("Please write at least a few words so we can find an accurate match!")
        else:
            with st.spinner("🔍 Analyzing your profile with AI..."):
                user_emb = embedder.encode([user_input])
                
                try:
                    # 1. Use the KNN model to predict the primary matched Category
                    cat_probs = knn_model.predict_proba(user_emb)[0]
                    top_cat_idx = np.argmax(cat_probs)
                    matched_category = le_career.inverse_transform([knn_model.classes_[top_cat_idx]])[0]
                    cat_score = cat_probs[top_cat_idx]
                except:
                    matched_category = "General"
                    cat_score = 0
                
                # 2. Use Semantic Similarity to find the specific Careers (Top 3)
                # This is much more accurate than a category classifier for specific roles
                similarities = cosine_similarity(user_emb, all_career_embs)[0]
                top_3_idx = np.argsort(similarities)[::-1][:3]
                
                # Get readiness for the embedding
                readiness_val = get_readiness(user_emb, None)
                
                st.markdown("---")
                
                # Display Matched Category prominently
                st.markdown(f"""
                <div style="background: rgba(102,126,234,0.1); border: 1px solid rgba(102,126,234,0.2); border-radius: 12px; padding: 20px; margin-bottom: 25px;">
                    <span style="color: #8888aa; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">Primary Match Category</span>
                    <h2 style="margin: 0; color: #f093fb !important;">{matched_category}</h2>
                </div>
                """, unsafe_allow_html=True)
                
                st.subheader("🌟 Your Top Career Matches")
                
                for idx, i in enumerate(top_3_idx):
                    row = df.iloc[[i]]
                    name = row['Career_Name'].values[0]
                    score = similarities[i]
                    render_card(name, row, rank=idx + 1, score=score, readiness_val=readiness_val if idx == 0 else None)


# ====== PAGE: CAREER DIRECTORY ======
elif page == "📚 Career Directory":
    st.markdown('<div class="hero-title">Career Directory</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Browse our comprehensive database of careers in Pakistan.</div>', unsafe_allow_html=True)
    
    # Sidebar Search / Filter in main area
    c1, c2, c3 = st.columns([2, 2, 3])
    cats = ["All Categories"] + sorted(df['Career_Category'].unique().tolist())
    sel_cat = c1.selectbox("Filter by Category", cats)
    
    filt_cat = df if sel_cat == "All Categories" else df[df['Career_Category'] == sel_cat]
    sel_career_list = filt_cat['Career_Name'].tolist()
    sel_career = c2.selectbox("Select Career", sel_career_list)
    
    search_query = c3.text_input("Search careers by name...", placeholder="e.g. Engineer, Doctor...")
    
    st.markdown("---")
    
    if search_query:
        # Fuzzy search or simple contain search
        search_results = df[df['Career_Name'].str.contains(search_query, case=False, na=False)]
        if not search_results.empty:
            for _, r in search_results.iterrows():
                # Need to pass row as a dataframe-like object or just adjust render_card
                # Since render_card expects row to be df[df['Career_Name'] == name]
                render_card(r['Career_Name'], df[df['Career_Name'] == r['Career_Name']])
        else:
            st.info(f"No careers found matching '{search_query}'.")
    elif sel_career:
        row = df[df['Career_Name'] == sel_career]
        render_card(sel_career, row)


# ====== PAGE: COMPARE CAREERS ======
elif page == "⚖️ Compare Careers":
    st.markdown('<div class="hero-title">Compare Careers</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Compare two careers side by side — salaries, education, and more.</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    names = df['Career_Name'].tolist()
    a = c1.selectbox("Career A", names, index=0)
    b = c2.selectbox("Career B", names, index=min(1, len(names)-1))
    
    if a and b:
        ra, rb = df[df['Career_Name']==a], df[df['Career_Name']==b]
        sa, sb = get_salary(a, ra['Career_Category'].values[0]), get_salary(b, rb['Career_Category'].values[0])
        
        st.markdown("---")
        
        # Salary comparison chart
        st.markdown("### 💰 Salary Comparison (PKR/month)")
        comp = pd.DataFrame({a: [sa.get("min",0), sa.get("avg",0), sa.get("max",0)],
                             b: [sb.get("min",0), sb.get("avg",0), sb.get("max",0)]},
                            index=["Minimum", "Average", "Maximum"])
        st.bar_chart(comp, color=["#667eea", "#f093fb"])
        
        # Side by side details
        c1, c2 = st.columns(2)
        for col, name, row, sal in [(c1,a,ra,sa), (c2,b,rb,sb)]:
            with col:
                st.markdown(f'<div class="compare-header"><strong style="color:#fff !important;">{name}</strong></div>', unsafe_allow_html=True)
                st.markdown(f"**Category:** {row['Career_Category'].values[0]}")
                st.markdown(f"**Salary:** PKR {fmt(sal['min'])} – {fmt(sal['max'])}/mo")
                st.markdown(f"**Intermediate:** {row['Intermediate_Path'].values[0]}")
                st.markdown(f"**Degree:** {row['Required_Degree'].values[0]}")
                st.markdown(f"**Description:** *{row['Description'].values[0]}*")
                with st.expander(f"📌 {name} Roadmap"):
                    for step in str(row['Roadmap'].values[0]).split(' | '):
                        st.markdown(f"- {step.strip()}")


# ====== PAGE: ABOUT ======
elif page == "ℹ️ About":
    st.markdown('<div class="hero-title">About CareerLens</div>', unsafe_allow_html=True)
    
    st.markdown("""
**CareerLens** is an AI-powered career guidance platform built specifically for Pakistani students and professionals.

### 🧠 How it Works
Your text input is converted into a mathematical embedding using **Sentence-Transformers** (`all-MiniLM-L6-v2`). 
This embedding is matched against 42 pre-computed career profiles using a **K-Nearest Neighbors** classifier to find 
your top career matches with confidence scores.

### 🇵🇰 Localized for Pakistan
- **Salary Ranges** in PKR
- **Educational Pathways** aligned with FSc, ICS, ICOM, FA boards
- **University Recommendations** across Punjab, Sindh, KPK, Balochistan & Islamabad
- **Step-by-step Roadmaps** from Matric to professional employment

### 🛠️ Models Used
| Model | Purpose |
|-------|---------|
| `all-MiniLM-L6-v2` | Converts text to semantic embeddings |
| `knn_model.pkl` | Finds nearest matching careers |
| `le_career.pkl` | Decodes predictions to career names |
| `readiness_model.pkl` | Predicts career readiness level |
| `career_embeddings.npy` | Pre-computed career profile embeddings |
| `salary_lookup.json` | Per-career salary ranges |
| `category_salary_fallback.json` | Category-level salary fallback |

### ⚙️ Tech Stack
`Streamlit` · `Scikit-Learn` · `Sentence-Transformers` · `Pandas` · `NumPy`
    """)
    st.info("🚀 Empowering the next generation of professionals in Pakistan.")
