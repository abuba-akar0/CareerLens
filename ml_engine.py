import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
from sentence_transformers import SentenceTransformer

@st.cache_resource(show_spinner="Loading AI Models & Data...")
def load_models_and_data():
    # 1. Load Models
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    knn = joblib.load('models/knn_model.pkl')
    le = joblib.load('models/le_career.pkl')
    
    try:
        readiness = joblib.load('models/readiness_model.pkl')
    except Exception as e:
        print(f"Warning: Readiness model not found or failed to load. {e}")
        readiness = None
        
    # 2. Load Data (Fixing the fillna bug)
    df = pd.read_csv('data/careers_pakistan.csv')
    df.fillna("", inplace=True) 
    
    # 3. Load Salaries
    with open('models/salary_lookup.json', 'r') as f:
        salary_lookup = json.load(f)
    with open('models/category_salary_fallback.json', 'r') as f:
        cat_salary = json.load(f)
        
    # 4. Generate Targeted Embeddings (Name + Keywords ONLY for dense matching)
    search_content = df['Career_Name'] + " " + df['Keywords']
    all_career_embs = embedder.encode(search_content.tolist())
    
    return embedder, knn, le, readiness, df, salary_lookup, cat_salary, all_career_embs

def get_salary(name, cat, salary_lookup, cat_salary):
    """Priority 1: Specific Career, Priority 2: Category Fallback"""
    s = salary_lookup.get(name)
    if not s:
        s = cat_salary.get(cat, {"min": 0, "avg": 0, "max": 0})
    return s

def calculate_readiness(readiness_model, s1, s2, s3, s4, s5):
    if readiness_model is None: 
        return 0
    features = np.array([[s1, s2, s3, s4, s5]])
    try:
        score = readiness_model.predict(features)[0]
        return min(max(score / 10.0, 0.0), 100.0) # Convert to 0-100%
    except Exception:
        return 0