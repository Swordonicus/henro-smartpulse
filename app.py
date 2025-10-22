import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page config
st.set_page_config(page_title="Henro SmartPulse™", layout="wide", page_icon="🎯")

# Custom CSS
st.markdown("""
<style>
    .main-header {font-size: 2.8rem; font-weight: 700; color: #1e3a8a; margin-bottom: 0;}
    .sub-header {font-size: 1.1rem; color: #64748b; margin-bottom: 2rem;}
    .kpi-card {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 1.5rem; border-radius: 0.5rem; color: white; text-align: center;}
    .alert-high {background-color: #fee; border-left: 4px solid #dc2626; padding: 1rem; margin: 0.5rem 0;}
    .alert-medium {background-color: #fffbeb; border-left: 4px solid #f59e0b; padding: 1rem; margin: 0.5rem 0;}
    .opportunity {background-color: #f0fdf4; border-left: 4px solid #10b981; padding: 1rem; margin: 0.5rem 0;}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">🎯 Henro SmartPulse™ Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered Customer, Market & Operations Cockpit</p>', unsafe_allow_html=True)

# Generate data
@st.cache_data
def load_data():
    np.random.seed(42)
    
    # Top 20 customers
    customers = [
        {"name": "AB InBev/Ecolab", "revenue": 84.0, "health": 68, "frequency": -22, "segment": "Brewing"},
        {"name": "RCL Foods", "revenue": 8.5, "health": 92, "frequency": 15, "segment": "Food"},
        {"name": "Tiger Brands", "revenue": 6.2, "health": 78, "frequency": 5, "segment": "Food"},
        {"name": "Clover Industries", "revenue": 4.8, "health": 85, "frequency": 8, "segment": "Dairy"},
        {"name": "Distell Group", "revenue": 3.9, "health": 72, "frequency": -8, "segment": "Beverages"},
        {"name": "AVI Limited", "revenue": 3.2, "health": 88, "frequency": 12, "segment": "Food"},
        {"name": "Sibanye-Stillwater", "revenue": 2.8, "health": 81, "frequency": 3, "segment": "Mining"},
        {"name": "Sasol Chemicals", "revenue": 2.4, "health": 76, "frequency": -5, "segment": "Chemicals"},
        {"name": "Omnia Holdings", "revenue": 2.1, "health": 83, "frequency": 7, "segment": "Chemicals"},
        {"name": "Nampak Ltd", "revenue": 1.9, "health": 79, "frequency": 2, "segment": "Packaging"},
        {"name": "Pioneer Foods", "revenue": 1.6, "health": 86, "frequency": 10, "segment": "Food"},
        {"name": "Astral Foods", "revenue": 1.4, "health": 74, "frequency": -3, "segment": "Poultry"},
        {"name": "Rand Water", "revenue": 1.2, "health": 91, "frequency": 18, "segment": "Water"},
        {"name": "Tongaat Hulett", "revenue": 0.98, "health": 69, "frequency": -12, "segment": "Sugar"},
        {"name": "Afgri Limited", "revenue": 0.85, "health": 82, "frequency": 6, "segment": "Agriculture"},
        {"name": "Chemtrade BW", "revenue": 0.72, "health": 87, "frequency": 11, "segment": "SADC"},
        {"name": "Zambian Chem", "revenue": 0.68, "health": 80, "frequency": 4, "segment": "SADC"},
        {"name": "Mozam Industrial", "revenue": 0.55, "health": 75, "frequency": -2, "segment": "SADC"},
        {"name": "Zim ChemCorp", "revenue": 0.48, "health": 84, "frequency": 9, "segment": "SADC"},
        {"name": "Namibia Traders", "revenue": 0.42, "health": 77, "frequency": 1, "segment": "SADC"}
    ]
    
    return pd.DataFrame(customers)

df = load_data()

# TOP BANNER - KPIs
st.markdown("### 📊 Executive KPI Summary")
col1, col2, col3, col4, col5, col6 = st.columns(6)

total_revenue = df["revenue"].sum()
pipeline_coverage = 2.8  # Mock
retention = 94.2  # Mock
ar_days = 147  # Mock
win_rate = 28.5  # Mock
ai_roi = 6.2  # Mock

with col1:
    st.metric("Revenue YTD", f"R{total_revenue:.1f}M", "+12.3%")
with col2:
    st.metric("Pipeline Coverage", f"{pipeline_coverage}x", "+0.4x")
with col3:
    st.metric("Retention Rate", f"{retention}%", "+2.1%")
with col4:
    st.metric("Avg AR Days", f"{ar_days}", "-18 days", delta_color="inverse")
with col5:
    st.metric("Win Rate", f"{win_rate}%", "+3.2%")
with col6:
    st.metric("AI ROI Tracker", f"{ai_roi}x", "+1.4x")

st.markdown("---")

# MIDDLE PANELS
col_left, col_right = st.columns([3, 2])

with col_left:
    # Customer Health Map
    st.markdown("### 🧭 Customer Health Map")
    st.markdown("*Color-coded: 🔴 High Risk | 🟡 Medium Risk | 🟢 Healthy*")
    
    # Add risk level
    df["risk"] = df["health"].apply(lambda x: "🔴 High Risk" if x < 70 else ("🟡 Medium" if x < 80 else "🟢 Healthy"))
    
    # Bubble chart
    fig = px.scatter(df, 
                     x="health", 
                     y="revenue",
                     size="revenue",
                     color="risk",
                     hover_name="name",
                     hover_data={"health": True, "revenue": True, "frequency": True, "risk": False},
                     color_discrete_map={"🟢 Healthy": "#10b981", "🟡 Medium": "#f59e0b", "🔴 High Risk": "#dc2626"},
                     title="Revenue vs Health Score (Bubble Size = Revenue)",
                     labels={"health": "Health Score", "revenue": "Annual Revenue (R Millions)"})
    
    fig.update_layout(height=400, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights
    high_risk = df[df["health"] < 70]
    if len(high_risk) > 0:
        st.markdown("**🚨 AI Insights:**")
        for _, row in high_risk.iterrows():
            if row["frequency"] < -15:
                st.markdown(f"- **{row['name']}**: Declining frequency ({row['frequency']}%). Consider pilot of Henrite® CIP system.")
            else:
                st.markdown(f"- **{row['name']}**: Health score {row['health']}/100. Schedule QBR within 7 days.")

with col_right:
    # Cross-Sell Opportunities
    st.markdown("### 💡 Cross-Sell Opportunities")
    st.markdown("*AI-ranked by propensity score*")
    
    opportunities = [
        {"customer": "Rand Water", "product": "Henrite® CIP", "score": 94, "value": "R850k"},
        {"customer": "RCL Foods", "product": "Progly® Enzymes", "score": 87, "value": "R620k"},
        {"customer": "Tiger Brands", "product": "Dinsel® Sanitizer", "score": 82, "value": "R480k"},
        {"customer": "Clover Industries", "product": "Henrite® Scale", "score": 79, "value": "R390k"},
        {"customer": "Pioneer Foods", "product": "Progly® Complete", "score": 76, "value": "R340k"},
        {"customer": "Astral Foods", "product": "Dinsel® Food Grade", "score": 71, "value": "R285k"},
        {"customer": "Sibanye-Stillwater", "product": "Industrial Caustic", "score": 68, "value": "R520k"},
        {"customer": "Omnia Holdings", "product": "Specialty Acids", "score": 64, "value": "R410k"},
    ]
    
    for opp in opportunities[:6]:
        st.markdown(f"""
        <div class="opportunity">
            <strong>{opp['customer']}</strong> → {opp['product']}<br>
            Propensity: {opp['score']}% | Est. Value: {opp['value']}
        </div>
        """, unsafe_allow_html=True)
    
    # Market Signals
    st.markdown("### 📈 Market Signals")
    st.info("""
    **🤖 AI Weekly Summary:**
    - Competitor "ChemSupply ZA" dropped Soda Ash prices by 8% (threat to 3 accounts)
    - New tender: Eskom R12M water treatment chemicals (deadline: 15 Nov)
    - Regulatory: NRCS updated citric acid standards (affects food clients)
    - SADC: Botswana import duties reduced 5% (opportunity for Chemtrade BW expansion)
    """)

st.markdown("---")

# BOTTOM ROW - Actions & Alerts
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🚨 Accounts Needing Attention")
    
    alerts = [
        {"customer": "AB InBev/Ecolab", "issue": "Payment 18 days overdue", "priority": "🔴 HIGH"},
        {"customer": "Tongaat Hulett", "issue": "Order frequency down 28%", "priority": "🔴 HIGH"},
        {"customer": "Distell Group", "issue": "Service ticket open 12 days", "priority": "🟡 MEDIUM"},
        {"customer": "Sasol Chemicals", "issue": "No contact in 52 days", "priority": "🟡 MEDIUM"},
        {"customer": "Astral Foods", "issue": "Contract renewal in 30 days", "priority": "🟡 MEDIUM"},
    ]
    
    for alert in alerts:
        if "HIGH" in alert["priority"]:
            st.markdown(f"""
            <div class="alert-high">
                <strong>{alert['priority']}</strong>: {alert['customer']}<br>
                {alert['issue']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="alert-medium">
                <strong>{alert['priority']}</strong>: {alert['customer']}<br>
                {alert['issue']}
            </div>
            """, unsafe_allow_html=True)

with col2:
    st.markdown("### 📋 Upcoming RFQs")
    
    rfqs = [
        {"client": "Eskom Water Treatment", "value": "R12M", "status": "✍️ Draft", "deadline": "15 Nov"},
        {"client": "Transnet Rail Maintenance", "value": "R4.5M", "status": "📤 Submitted", "deadline": "22 Nov"},
        {"client": "City of Joburg - Waste", "value": "R3.2M", "status": "⏳ Pending", "deadline": "8 Dec"},
        {"client": "SAB Brewery Expansion", "value": "R8.7M", "status": "✍️ Draft", "deadline": "12 Dec"},
        {"client": "Woolworths DC Cleaning", "value": "R2.1M", "status": "📤 Submitted", "deadline": "20 Dec"},
    ]
    
    for rfq in rfqs:
        color = "#fef3c7" if "Draft" in rfq["status"] else ("#dbeafe" if "Submitted" in rfq["status"] else "#fce7f3")
        st.markdown(f"""
        <div style="background-color: {color}; padding: 0.8rem; margin: 0.5rem 0; border-radius: 0.3rem;">
            <strong>{rfq['client']}</strong> - {rfq['value']}<br>
            Status: {rfq['status']} | Due: {rfq['deadline']}
        </div>
        """, unsafe_allow_html=True)

with col3:
    st.markdown("### 💰 Finance Pulse")
    
    # Cash flow mini chart
    dates = pd.date_range(end=datetime.now(), periods=12, freq='W')
    cash_flow = [2.4, 2.1, 2.8, 2.3, 2.6, 2.9, 2.2, 2.7, 3.1, 2.5, 2.8, 3.0]
    
    fig_cash = go.Figure()
    fig_cash.add_trace(go.Scatter(
        x=dates, y=cash_flow,
        mode='lines+markers',
        name='Cash Position',
        line=dict(color='#10b981', width=3)
    ))
    fig_cash.add_hline(y=2.5, line_dash="dash", line_color="red", 
                       annotation_text="Target: R2.5M")
    fig_cash.update_layout(height=250, showlegend=False, 
                          title="Weekly Cash Position (R Millions)",
                          xaxis_title="", yaxis_title="R Millions")
    st.plotly_chart(fig_cash, use_container_width=True)
    
    # DSO metrics
    st.metric("DSO (Days Sales Outstanding)", "147 days", "-18 days", delta_color="inverse")
    st.metric("Variance vs Target (90 days)", "+57 days", "-18 days", delta_color="inverse")
    
    st.markdown("**Action Items:**")
    st.markdown("- 🔴 AB InBev: R14.2M overdue 18 days")
    st.markdown("- 🟡 Distell: R780k overdue 12 days")

# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: #64748b; padding: 1rem;'>
    <strong>Henro SmartPulse™</strong> | AI-Powered Business Intelligence<br>
    Last Updated: {datetime.now().strftime('%d %B %Y, %H:%M')}<br>
    <em>This is a Phase 1 demonstration. Full system includes real-time CRM integration, 
    predictive models, and automated alerts.</em>
</div>
""", unsafe_allow_html=True)
