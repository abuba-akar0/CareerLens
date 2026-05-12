import streamlit as st
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from ml_engine import load_models_and_data
from ui_components import load_custom_css, render_card

# st.set_page_config(page_title="AI Matcher", page_icon="🎯", layout="wide")
load_custom_css()

# Load Engine
try:
    embedder, knn_model, le_career, _, df, salary_lookup, cat_salary, all_career_embs = load_models_and_data()
except Exception as e:
    st.error("Error loading AI Engine. Please check your models folder.")
    st.stop()

st.markdown('<div class="hero-title">Find Your Dream Career</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Choose how you want to find your match!</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["✍️ Type Your Interests", "🧭 Take the Career Compass Quiz"])

final_search_query = None

# TAB 1: TEXT MATCHING
with tab1:
    tag_options = {
        "💻 Technology & Coding": "programming software coding computer algorithms data",
        "🏥 Healthcare & Medicine": "biology medicine patient health clinical hospital",
        "🧮 Finance & Accounting": "accounting finance numbers audit taxation ICAP",
        "📈 Business & Marketing": "business marketing management strategy sales brand",
        "⚙️ Engineering & Construction": "physics mathematics engineering design construction",
        "🎨 Design & Creativity": "creative design graphics visual art media",
        "⚖️ Law & Civil Services": "law courts CSS government policy justice",
        "📚 Education & Media": "teaching journalism writing communication media"
    }
    
    selected_tags = st.multiselect("Select your areas of interest (Optional):", options=list(tag_options.keys()))
    user_input = st.text_area("Tell us about yourself...", height=120, placeholder="e.g., I want to solve real world problems using AI and computer vision.", label_visibility="collapsed")
    
    if st.button("Find My Career Match 🚀", key="btn_text", type="primary"):
        if len(user_input.split()) < 3 and not selected_tags:
            st.warning("Please provide a bit more detail or select some tags!")
        else:
            query = user_input.lower()
            
            # The Fixed Expander Logic
            expander_dict = {
                "army": "CSS government civil service management leadership",
                "military": "CSS government civil service management leadership defence",
                "cricket": "physical health management fitness coaching sports athlete",
                "youtuber": "media communication creative digital marketing influencer content creator",
                "chef": "business management hospitality creative food cooking culinary",
                "astronaut": "physics engineering mathematics science astronomy space rocket",
                "pilot": "physics engineering mathematics science aviation aerospace flying planes",
                "fly": "physics engineering mathematics science aviation aerospace",
                "llm": "artificial intelligence machine learning data science python coding ai",
                "history": "law social sciences policy making civil services culture writing"
            }
            
            input_words = query.split()
            for trigger, expansion in expander_dict.items():
                if trigger in input_words:
                    query += f" {expansion}"
                    
            for tag in selected_tags:
                query += f" {tag_options[tag]}"
                
            final_search_query = query

# TAB 2: COMPASS QUIZ
with tab2:
    st.markdown("### 🧭 The Career Compass")
    st.write("Answer these 4 questions to let our AI build your perfect professional profile.")
    
    q_subjects = st.pills("1. Which topics naturally fascinate you?", ["💻 Computers, Software & Tech", "⚙️ Physics, Machines & Engineering", "🧬 Biology, Anatomy & Medicine", "🎨 Art, Design & Digital Media", "📊 Business, Markets & Economics", "⚖️ Law, History & Society"], selection_mode="multi")
    q_style = st.pills("2. How do you prefer to solve problems?", ["Deep Focus / Solo Coding", "Analyzing Data / Researching", "Brainstorming / Creative Thinking", "Leading / Managing Teams", "Hands-on / Physical Work", "Directly Helping/Treating People"])
    q_env = st.pills("3. What is your dream work environment?", ["A modern tech office or remote from home 🏠", "A hospital, clinic, or medical lab 🏥", "A corporate high-rise or financial firm 🏢", "Outdoors, on a site, or traveling 🌍", "A creative studio or production set 🎬"])
    q_goal = st.pills("4. What is your ultimate career goal?", ["Inventing new technologies and software", "Healing patients and saving lives", "Building a massive business or global brand", "Designing beautiful interfaces or creating content", "Defending justice and shaping national policy", "Engineering advanced machines or infrastructure", "Managing wealth and global finances"])

    if st.button("Match via Compass Quiz 🎯", key="btn_quiz", type="primary"):
        if not q_subjects or not q_style or not q_env or not q_goal:
            st.warning("Please answer all the questions so we can find your perfect match!")
        else:
            quiz_keywords = []
            for sub in q_subjects:
                if "Computers" in sub: quiz_keywords.append("python software coding cloud architecture web3 algorithms database IT")
                if "Physics" in sub: quiz_keywords.append("calculus thermodynamics aerodynamics robotics mechatronics AutoCAD construction")
                if "Biology" in sub: quiz_keywords.append("anatomy kinesiology biochemistry surgery patient therapy genetics")
                if "Art" in sub: quiz_keywords.append("ui/ux figma typography premiere pro visual storytelling digital media")
                if "Business" in sub: quiz_keywords.append("marketing seo strategy commerce entrepreneurship startup digital advertising")
                if "Law" in sub: quiz_keywords.append("sociology public policy justice international relations debate civil service")

            if "Solo Coding" in q_style: quiz_keywords.append("independent analytical remote deep-focus")
            elif "Researching" in q_style: quiz_keywords.append("data-driven methodical objective detail-oriented")
            elif "Creative" in q_style: quiz_keywords.append("innovative creative fast-paced visual")
            elif "Leading" in q_style: quiz_keywords.append("collaborative leadership charismatic strategic")
            elif "Hands-on" in q_style: quiz_keywords.append("experimental hands-on physical dynamic")
            elif "Helping" in q_style: quiz_keywords.append("empathetic patient-focused communication")

            if "tech" in q_env: quiz_keywords.append("software web cloud artificial intelligence server")
            elif "hospital" in q_env: quiz_keywords.append("medicine clinical therapy healthcare lab")
            elif "corporate" in q_env: quiz_keywords.append("finance accounting investment corporate business bank")
            elif "Outdoors" in q_env: quiz_keywords.append("civil engineering aerospace aviation architecture site")
            elif "studio" in q_env: quiz_keywords.append("media content creation film journalism design audio")

            if "technologies" in q_goal: quiz_keywords.append("build secure apps innovate enterprise infrastructure")
            elif "Healing" in q_goal: quiz_keywords.append("rehabilitation treat patients clinic sports medicine")
            elif "business" in q_goal: quiz_keywords.append("chief marketing officer run agency global campaigns")
            elif "beautiful" in q_goal: quiz_keywords.append("design intuitive apps product designer audience")
            elif "justice" in q_goal: quiz_keywords.append("draft policies advise government NGO public opinion")
            elif "Engineering" in q_goal: quiz_keywords.append("design next-gen autonomous systems industrial solutions")
            elif "wealth" in q_goal: quiz_keywords.append("fintech trading systems product manager")

            final_search_query = " ".join(quiz_keywords)

# --- EXECUTE AI PIPELINE (Runs if either tab submitted) ---
if final_search_query:
    with st.spinner("Analyzing your profile..."):
        user_emb = embedder.encode([final_search_query])
        
        # 1. KNN Category Match
        try:
            cat_probs = knn_model.predict_proba(user_emb)[0]
            matched_category = le_career.inverse_transform([knn_model.classes_[np.argmax(cat_probs)]])[0]
        except Exception:
            matched_category = "General"
            
        # 2. SBERT Semantic Match
        similarities = cosine_similarity(user_emb, all_career_embs)[0]
        max_sim = np.max(similarities)
        top_3_idx = np.argsort(similarities)[::-1][:3]
        
        st.markdown("---")
        
        # 3. Dynamic Threshold Handling
        if max_sim < 0.15:
            st.markdown("""
            <div style="background: rgba(255,71,87,0.1); border: 1px solid rgba(255,71,87,0.3); border-radius: 12px; padding: 20px; text-align: center;">
                <h3 style="color: #ff4757; margin-top: 0;">We couldn't find a strong match 🕵️‍♂️</h3>
                <p style="color: #e0e0e0; margin-bottom: 0;">It looks like your interest might be outside our core Pakistani career dataset. Try exploring the Directory or adding more specific skills/tags!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.expander("🤖 AI Confidence Details"):
                if max_sim < 0.25:
                    st.warning("⚠️ Low Confidence Match: We found some related fields, but they might not be a perfect fit.")
                st.write(f"Top Similarity Score: **{max_sim*100:.1f}%**")
                
            st.markdown(f"""
            <div style="background: rgba(102,126,234,0.1); border: 1px solid rgba(102,126,234,0.2); border-radius: 12px; padding: 20px; margin-bottom: 30px; text-align: center;">
                <span style="color: #8888aa; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px;">Predicted Category Match</span>
                <h2 style="margin: 5px 0 0 0; color: #f093fb !important;">{matched_category}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            st.subheader("🌟 Top 3 Career Matches")
            for rank, i in enumerate(top_3_idx):
                row = df.iloc[[i]]
                name = row['Career_Name'].values[0]
                render_card(name, row, salary_lookup, cat_salary, rank=rank+1, score=similarities[i])