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
    
    st.markdown("<p style='font-size:0.95rem; color:#f3f4f6; margin-bottom:5px;'>💡 <b>Try an Example Prompt:</b></p>", unsafe_allow_html=True)
    
    example_prompts = [
        "I love mathematics and want to build modern tech infrastructure.",
        "I want to help patients recover from physical injuries.",
        "I enjoy analyzing financial data and creating business strategies.",
        "I am creative, love designing interfaces, and want to work remotely."
    ]
    
    selected_example = st.pills("Examples", example_prompts, selection_mode="single", label_visibility="collapsed")
    default_text = selected_example if selected_example else ""
    
    user_input = st.text_area("Tell us about yourself...", value=default_text, height=120, placeholder="e.g., I want to solve real world problems using AI and computer vision.", label_visibility="collapsed")
    
    if st.button("Find My Career Match 🚀", key="btn_text", type="primary"):
        word_list = user_input.split()
        if len(word_list) < 3 and not selected_tags:
            st.warning("Please provide a bit more detail or select some tags!")
        else:
            # --- NEW FIX: GIBBERISH PATTERN FILTER (WORD-BOUNDED) ---
            import re
            clean_text = user_input.lower().strip()
            word_list = clean_text.split()
            
            # 1. Check for long sequences of consecutive consonants WITHIN individual words
            consonant_sequences = any(re.search(r'[bcdfghjklmnpqrstvwxz]{5,}', word) for word in word_list)
            
            # 2. Check for impossible English vowel clusters (Whole word matching)
            impossible_vowels = ["uiop", "iooo", "eeee", "aaaa", "uuu"]
            has_impossible_vowels = any(cluster in clean_text for cluster in impossible_vowels)
            
            # 3. FIX: Keyboard smash rows now require word boundaries (\b) so they don't trip on real words
            keyboard_smash_patterns = [r'\basdf', r'sdfg', r'dfgh', r'ghjk', r'hjkl\b', r'\bqwerty\b']
            has_keyboard_smash = any(re.search(pattern, clean_text) for pattern in keyboard_smash_patterns)

            if (consonant_sequences or has_impossible_vowels or has_keyboard_smash) and not selected_tags:
                st.error("🔍 **Invalid Input Detected**")
                st.warning("Your text matches common keyboard smashing patterns or random noise. Please type real educational or career keywords.")
                st.stop() # Force execution to halt immediately for gibberish
                
            query = clean_text
            
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
                    
            # --- NEW FIX: EXACT WORD CONTEXT-AWARE INFRASTRUCTURE ---
            if "infrastructure" in query:
                import re
                # Use \b to ensure we match whole words only (prevents 'networks' from matching 'network')
                tech_pattern = r'\b(tech|computer|software|digital|networking)\b'
                civil_pattern = r'\b(civil|build|bridge|road|city|construction|dam|transit|networks)\b'
                
                if re.search(tech_pattern, query):
                    query += " cloud devops server networking backend database datacenter computing computing systems"
                elif re.search(civil_pattern, query):
                    query += " construction architectural structures concrete materials highways public works engineering"
                    
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
        raw_similarities = cosine_similarity(user_emb, all_career_embs)[0]
        top_3_idx = np.argsort(raw_similarities)[::-1][:3]
        raw_top_score = float(raw_similarities[top_3_idx[0]])
        
        st.markdown("---")
        
        # 3. Direct Raw Threshold Gate
        if raw_top_score < 0.22:
            st.error("🕵️‍♂️ **Out of Scope!**\n\nWe couldn't find a strong match. Your query seems outside our core Pakistani career dataset or is too brief to understand. Please try again with more relevant professional keywords.")
            st.stop()
            
        # --- NON-LINEAR SMOOTH SCALING ---
        def scale_score(raw_val):
            if raw_val >= 0.60:
                return min(int(90 + ((raw_val - 0.60) / 0.40) * 9), 99)
            elif raw_val >= 0.22:
                # Map 0.22-0.60 to 50-90%
                return int(50 + ((raw_val - 0.22) / 0.38) * 40)
            return int((raw_val / 0.22) * 49)
            
        # Scale the full array for UI consistency
        similarities = np.array([scale_score(val) / 100.0 for val in raw_similarities])
        calibrated_score = int(similarities[top_3_idx[0]] * 100)
            
        with st.expander("🤖 AI Confidence Details"):
            if calibrated_score < 60:
                st.warning("⚠️ Moderate Confidence Match: We found some related fields, but they might not be a perfect fit.")
            st.write(f"Top Calibrated Similarity Score: **{calibrated_score}%** (Raw Score: {raw_top_score:.3f})")
            
        # FIX: Explicitly tie the category header to the rank-1 semantic match
        if len(top_3_idx) > 0:
            top_row = df.iloc[[top_3_idx[0]]]
            if not top_row.empty:
                matched_category = top_row['Career_Category'].values[0]
                
        st.markdown(f"""
        <div style="background: rgba(102,126,234,0.1); border: 1px solid rgba(102,126,234,0.2); border-radius: 12px; padding: 20px; margin-bottom: 30px; text-align: center;">
            <span style="color: #8888aa; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px;">Predicted Category Match</span>
            <h2 style="margin: 5px 0 0 0; color: #f093fb !important;">{matched_category}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("🌟 Top 3 Career Matches")
        for rank, i in enumerate(top_3_idx):
            row = df.iloc[[i]]
            # Safe UI Components Loop Iterations with bounds filter
            if not row.empty:
                name = row['Career_Name'].values[0]
                # Pass safe dictionary variables
                render_card(name, row, salary_lookup, cat_salary, rank=rank+1, score=similarities[i])