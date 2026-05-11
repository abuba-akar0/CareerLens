# 🎓 CareerLens Pakistan

> AI-powered career guidance platform built for Pakistani students and professionals.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit&logoColor=white)
![ML](https://img.shields.io/badge/ML-Scikit--Learn-F7931E?logo=scikit-learn&logoColor=white)

## ✨ Features

- **🎯 AI Career Matcher** — Describe your interests in natural language and get top 3 career matches with confidence scores
- **📚 Career Directory** — Browse and filter 42 careers across 8 categories
- **⚖️ Career Comparison** — Compare any two careers side-by-side with salary charts
- **🎓 Readiness Assessment** — AI-predicted readiness score for your top match
- **🏫 University Finder** — Province-wise university recommendations (Punjab, Sindh, KPK, Balochistan, Islamabad)
- **📌 Step-by-Step Roadmaps** — From Matriculation to professional employment
- **💰 Salary Insights** — Visual salary breakdowns with min/avg/max charts

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | [Streamlit](https://streamlit.io/) |
| NLP Embeddings | [Sentence-Transformers](https://www.sbert.net/) (`all-MiniLM-L6-v2`) |
| ML Classification | Scikit-Learn (KNN Classifier) |
| Data | Pandas, NumPy |

## 📦 Project Structure

```
CareerLens/
├── app.py                              # Main Streamlit application
├── requirements.txt                    # Python dependencies
├── data/
│   └── careers_pakistan.csv            # 42 careers with full metadata
└── models/
    ├── knn_model.pkl                  # KNN career classifier
    ├── le_career.pkl                  # Label encoder for career names
    ├── readiness_model.pkl            # Career readiness predictor
    ├── career_embeddings.npy          # Pre-computed career embeddings
    ├── salary_lookup.json             # Per-career salary data
    └── category_salary_fallback.json  # Category-level salary fallback
```

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/your-username/CareerLens.git
cd CareerLens

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

The app opens at `http://localhost:8501`.

> **Note:** The `all-MiniLM-L6-v2` model (~80MB) downloads automatically on first run and is cached locally.

## 🤝 Contributing

<<<<<<< HEAD
Contributions, issues, and feature requests are welcome!
=======
Contributions, issues, and feature requests are welcome!
>>>>>>> 236b7ee939c2bfe66ce1632df97e80cbc5dcbb05
