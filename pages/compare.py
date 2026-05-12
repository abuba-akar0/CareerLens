import streamlit as st
import pandas as pd
import altair as alt
from ml_engine import load_models_and_data, get_salary
from ui_components import load_custom_css, render_card

# st.set_page_config(page_title="Compare Careers", page_icon="⚖️", layout="wide")
load_custom_css()

_, _, _, _, df, salary_lookup, cat_salary, _ = load_models_and_data()

st.markdown('<div class="hero-title">Compare Careers</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Side-by-side analysis of salaries, education, and paths.</div>', unsafe_allow_html=True)

names = sorted(df['Career_Name'].tolist())
c1, c2 = st.columns(2)
a = c1.selectbox("Career A", names, index=0)
b = c2.selectbox("Career B", names, index=min(1, len(names)-1))

if a and b:
    ra, rb = df[df['Career_Name']==a], df[df['Career_Name']==b]
    sa, sb = get_salary(a, ra['Career_Category'].values[0], salary_lookup, cat_salary), get_salary(b, rb['Career_Category'].values[0], salary_lookup, cat_salary)
    
    st.markdown("---")
    st.markdown("### 💰 Salary Comparison")
    
    comp_data = []
    for metric, val_a, val_b in zip(["Minimum", "Average", "Maximum"], 
                                    [sa['min'], sa['avg'], sa['max']], 
                                    [sb['min'], sb['avg'], sb['max']]):
        comp_data.append({"Metric": metric, "Career": a, "Salary (PKR)": val_a})
        comp_data.append({"Metric": metric, "Career": b, "Salary (PKR)": val_b})
        
    comp_df = pd.DataFrame(comp_data)
    
    chart = alt.Chart(comp_df).mark_bar().encode(
        x=alt.X('Career:N', title=None, axis=alt.Axis(labels=False, ticks=False)),
        y=alt.Y('Salary (PKR):Q', axis=alt.Axis(format="s", gridColor="rgba(255,255,255,0.1)")),
        color=alt.Color('Career:N', scale=alt.Scale(range=["#667eea", "#f093fb"]), legend=alt.Legend(title="Careers", orient="top")),
        column=alt.Column('Metric:N', sort=["Minimum", "Average", "Maximum"], header=alt.Header(title=None, labelColor="#ffffff", labelFontSize=14))
    ).properties(width=200, height=350).configure_view(stroke="transparent").configure_axis(labelColor="#c8c8d4", titleColor="#c8c8d4")
    
    st.altair_chart(chart)
    
    st.markdown("### 🎓 Educational Pathway Comparison")
    st.markdown(f"""
    <table style="width:100%; border-collapse: collapse; margin-bottom: 30px;">
        <tr style="background: rgba(255,255,255,0.05);">
            <th style="padding: 15px; border: 1px solid rgba(255,255,255,0.1); text-align: left; color:#f093fb;">Feature</th>
            <th style="padding: 15px; border: 1px solid rgba(255,255,255,0.1); text-align: left; width: 40%; color:#667eea; font-size:1.1rem;">{a}</th>
            <th style="padding: 15px; border: 1px solid rgba(255,255,255,0.1); text-align: left; width: 40%; color:#667eea; font-size:1.1rem;">{b}</th>
        </tr>
        <tr>
            <td style="padding: 15px; border: 1px solid rgba(255,255,255,0.1); font-weight: bold;">Required Degree</td>
            <td style="padding: 15px; border: 1px solid rgba(255,255,255,0.1);">{ra['Required_Degree'].values[0]}</td>
            <td style="padding: 15px; border: 1px solid rgba(255,255,255,0.1);">{rb['Required_Degree'].values[0]}</td>
        </tr>
        <tr style="background: rgba(255,255,255,0.02);">
            <td style="padding: 15px; border: 1px solid rgba(255,255,255,0.1); font-weight: bold;">Intermediate Path</td>
            <td style="padding: 15px; border: 1px solid rgba(255,255,255,0.1);">{ra['Intermediate_Path'].values[0]}</td>
            <td style="padding: 15px; border: 1px solid rgba(255,255,255,0.1);">{rb['Intermediate_Path'].values[0]}</td>
        </tr>
        <tr>
            <td style="padding: 15px; border: 1px solid rgba(255,255,255,0.1); font-weight: bold;">Core Skills / Keywords</td>
            <td style="padding: 15px; border: 1px solid rgba(255,255,255,0.1); font-size: 0.9em; color: #f3f4f6;">{ra['Keywords'].values[0]}</td>
            <td style="padding: 15px; border: 1px solid rgba(255,255,255,0.1); font-size: 0.9em; color: #f3f4f6;">{rb['Keywords'].values[0]}</td>
        </tr>
    </table>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📋 Deep Dive Cards")
    col1, col2 = st.columns(2)
    with col1:
        render_card(a, ra, salary_lookup, cat_salary)
    with col2:
        render_card(b, rb, salary_lookup, cat_salary)