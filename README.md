# 🎓 CareerLens Pakistan

**CareerLens** is an AI-powered career guidance platform specifically designed for the Pakistani professional landscape. It leverages modern machine learning techniques to help students and professionals navigate their career paths with data-driven insights.

![CareerLens Banner](https://img.shields.io/badge/AI--Powered-Career--Guidance-blueviolet?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit)
![Python](https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=Python)

---

## 🚀 Key Features

### 🎯 AI Matcher
- **Semantic Search**: Describe your interests in natural language, and our **SBERT** (Sentence-BERT) engine finds the closest matches in our local dataset.
- **Career Compass Quiz**: A minimalist, intuitive "Apple-style" quiz using modern UI components (`st.pills`) to profile your professional personality.

### 📊 Readiness Assessment
- **Score Prediction**: A linear regression model calculates your professional readiness based on 5 key dimensions.
- **Visual Feedback**: Interactive **Plotly Gauge Charts** provide instant visual feedback on your preparation level.
- **Actionable Advice**: Receive dynamic, personalized guidance to bridge your skill gaps.

### 📚 Career Directory
- Browse a comprehensive database of **74+ careers** tailored to Pakistan.
- Detailed roadmaps, educational requirements, and top universities in every province.

### ⚖️ Career Comparison
- Side-by-side analysis of salary expectations (Min/Avg/Max).
- Comparative educational pathways and required degree grids.

---

## 🛠️ Technology Stack

- **Frontend**: [Streamlit](https://streamlit.io/) (with custom Glassmorphism CSS)
- **AI Engine**: 
  - `Sentence-Transformers` (SBERT) for semantic matching.
  - `Scikit-learn` (KNN for category classification, Linear Regression for readiness).
- **Data Visualization**: [Plotly](https://plotly.com/) & [Altair](https://altair-viz.github.io/).
- **Data Handling**: `Pandas` & `NumPy`.

---

## 📦 Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/abuba-akar0/CareerLens.git
   cd CareerLens
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   streamlit run app.py
   ```

---

## 📂 Project Structure

```text
├── app.py              # Main entry point & Home page
├── ml_engine.py        # AI logic, Model loading & Data processing
├── ui_components.py    # Shared UI elements & Custom CSS
├── data/               # Local datasets (CSV)
├── models/             # Trained ML models (.pkl) & Salary lookups
├── pages/              # Multi-page application modules
└── requirements.txt    # Project dependencies
```

---

## 🎨 Design Philosophy

CareerLens follows a **Minimalistic & Intuitive** design system:
- **Glassmorphism**: Premium frosted-glass UI elements for a modern feel.
- **High Contrast**: Optimized for readability with a sleek dark-themed palette.
- **HCI Optimized**: Reduced cognitive load by hiding technical jargon and focusing on actionable insights.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Built with ❤️ for the future of Pakistan.*
