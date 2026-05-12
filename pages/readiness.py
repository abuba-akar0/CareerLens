import streamlit as st
from ml_engine import load_models_and_data, calculate_readiness
from ui_components import load_custom_css

# st.set_page_config(page_title="Readiness Assessment", page_icon="📊", layout="wide")
load_custom_css()

_, _, _, readiness_model, _, _, _, _ = load_models_and_data()

st.markdown('<div class="hero-title">Career Readiness</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Rate your skills on 5 key dimensions to see your overall career readiness percentage.</div>', unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("### Self-Assessment Form")
    c1, c2 = st.columns(2)
    s1 = c1.slider("Academic Performance", 0, 10, 5, help="weight 20.4%")
    s2 = c2.slider("Technical Skills", 0, 10, 5, help="weight 20.0%")
    s3 = c1.slider("Extracurricular Activities", 0, 10, 5, help="weight 9.9%")
    s4 = c2.slider("Communication / Soft Skills", 0, 10, 5, help="weight 9.9%")
    s5 = st.slider("Career Goal Clarity", 0, 10, 5, help="weight 39.8%")
    
    if st.button("Calculate Readiness Score", type="primary"):
        score = calculate_readiness(readiness_model, s1, s2, s3, s4, s5)
        color = "#2ed573" if score > 70 else "#ffa502" if score > 40 else "#ff4757"
        
        st.markdown("---")
        
        col_chart, col_advice = st.columns([1, 1])
        
        with col_chart:
            import plotly.graph_objects as go
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Readiness Score", 'font': {'color': '#f3f4f6'}},
                number = {'suffix': "%", 'font': {'color': color}},
                gauge = {
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "rgba(255,255,255,0.5)"},
                    'bar': {'color': color},
                    'bgcolor': "rgba(255,255,255,0.05)",
                    'borderwidth': 0,
                    'steps': [
                        {'range': [0, 40], 'color': 'rgba(255,71,87,0.1)'},
                        {'range': [40, 70], 'color': 'rgba(255,165,2,0.1)'},
                        {'range': [70, 100], 'color': 'rgba(46,213,115,0.1)'}],
                }
            ))
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=300,
                margin=dict(l=20, r=20, t=50, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col_advice:
            st.markdown("### 💡 Actionable Advice")
            
            if s5 < 6:
                st.info("🎯 **Low Goal Clarity:** You seem unsure about your path. Try our **AI Matcher** quiz to narrow down your options based on your interests.")
            if s2 < 6:
                st.warning("💻 **Technical Gap:** The modern job market requires hard skills. Consider taking an online course in Python, Data, or Design depending on your field.")
            if s4 < 6:
                st.warning("🗣️ **Soft Skills Needed:** Communication is just as important as technical ability. Look for presentation or debate opportunities to build confidence.")
            if s1 < 6:
                st.warning("📚 **Academic Focus:** Your academics might need a boost. Focus on improving your core subject grades.")
            
            if score >= 75:
                st.success("🌟 **Outstanding!** You are highly prepared for the professional world. Keep up the excellent work and start exploring top-tier roles in our Directory.")
            elif score >= 50 and score < 75:
                st.info("👍 **On Track!** You have a solid foundation. Focus on the specific areas mentioned above to become a top-tier candidate.")
            else:
                st.error("🚀 **Time to Step Up!** You have significant room for improvement. Take action now using the advice above.")