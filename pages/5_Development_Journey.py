import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page Config
st.set_page_config(
    page_title="Development Journey",
    page_icon="🗺️",
    layout="wide"
)

# Title
st.markdown("""
    <div style='text-align: center;'>
        <h1 style='color: #064E3B;'>
            🗺️ Project Development Journey
        </h1>
        <p style='color: #444444; font-size: 18px;'>
            From March 2026 to May 2026
        </p>
    </div>
""", unsafe_allow_html=True)
st.divider()

# Project Stats
st.subheader("📊 Project At A Glance")

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.metric("⏱️ Duration", "3 Months")
with c2:
    st.metric("📋 Total Tasks", "9 Tasks")
with c3:
    st.metric("🤖 ML Models", "3 Models")
with c4:
    st.metric("📄 App Pages", "5 Pages")
with c5:
    st.metric("✅ Status", "Completed")

st.divider()

# Gantt Chart Data
st.subheader("📅 Project Gantt Chart")

timeline_data = pd.DataFrame([
    dict(
        Task="Research & Dataset Selection",
        Start="2026-03-01",
        Finish="2026-03-14",
        Phase="Planning",
        Details="Selected Hotel Booking Demand dataset from Kaggle and Energy Efficiency dataset from UCI"
    ),
    dict(
        Task="Data Cleaning & Exploration",
        Start="2026-03-10",
        Finish="2026-03-28",
        Phase="Data Engineering",
        Details="Cleaned 119,390 records, handled missing values, removed outliers and invalid bookings"
    ),
    dict(
        Task="Feature Engineering",
        Start="2026-03-25",
        Finish="2026-04-08",
        Phase="Data Engineering",
        Details="Created 8 new features including total guests, season, lead time category and revenue lost"
    ),
    dict(
        Task="ML Model Building",
        Start="2026-04-05",
        Finish="2026-04-20",
        Phase="AI Development",
        Details="Built and compared 3 models: Logistic Regression, Random Forest and XGBoost"
    ),
    dict(
        Task="Energy Calculator Development",
        Start="2026-04-15",
        Finish="2026-04-28",
        Phase="AI Development",
        Details="Built unique energy saving calculator connecting ML predictions to KWh and CO2 savings"
    ),
    dict(
        Task="Streamlit UI Development",
        Start="2026-04-25",
        Finish="2026-05-05",
        Phase="Frontend",
        Details="Built 5 page professional web application with interactive charts and dashboards"
    ),
    dict(
        Task="Data Visualizations",
        Start="2026-04-28",
        Finish="2026-05-08",
        Phase="Frontend",
        Details="Created 15+ interactive Plotly charts including heatmaps, bar charts and scatter plots"
    ),
    dict(
        Task="System Testing",
        Start="2026-05-05",
        Finish="2026-05-12",
        Phase="Testing",
        Details="Unit testing, integration testing and model performance testing completed"
    ),
    dict(
        Task="Technical Report Writing",
        Start="2026-05-08",
        Finish="2026-05-18",
        Phase="Submission",
        Details="Wrote 2300 word technical report covering product design, development and project management"
    ),
])

# Plot Gantt Chart
fig = px.timeline(
    timeline_data,
    x_start="Start",
    x_end="Finish",
    y="Task",
    color="Phase",
    title="Project Development Timeline (March - May 2026)",
    color_discrete_map={
        "Planning":         "#10B981",
        "Data Engineering": "#F59E0B",
        "AI Development":   "#064E3B",
        "Frontend":         "#34D399",
        "Testing":          "#FBBF24",
        "Submission":       "#059669"
    },
    hover_data=["Details"]
)

fig.update_yaxes(autorange="reversed")
fig.update_xaxes(range=["2026-03-01", "2026-05-20"])
fig.update_layout(
    height=500,
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    font=dict(size=13)
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# Phase Details
st.subheader("📋 Development Phases Details")

phases = [
    {
        "emoji": "🟢",
        "phase": "Phase 1 — Planning",
        "dates": "March 1 - March 14, 2026",
        "color": "#D1FAE5",
        "border": "#10B981",
        "tasks": [
            "Researched suitable open source datasets",
            "Selected Hotel Booking Demand from Kaggle",
            "Selected Energy Efficiency from UCI",
            "Defined project scope and objectives",
            "Set up Python development environment"
        ]
    },
    {
        "emoji": "🟡",
        "phase": "Phase 2 — Data Engineering",
        "dates": "March 10 - April 8, 2026",
        "color": "#FEF3C7",
        "border": "#F59E0B",
        "tasks": [
            "Loaded and explored 119,390 booking records",
            "Handled missing values in 4 columns",
            "Removed invalid bookings with zero guests",
            "Removed outliers in average daily rate",
            "Created 8 new feature engineered columns",
            "Created season and lead time categories"
        ]
    },
    {
        "emoji": "🟢",
        "phase": "Phase 3 — AI Development",
        "dates": "April 5 - April 28, 2026",
        "color": "#D1FAE5",
        "border": "#10B981",
        "tasks": [
            "Built Logistic Regression baseline model",
            "Built Random Forest with 100 estimators",
            "Built XGBoost with gradient boosting",
            "Compared all 3 models on test set",
            "Selected XGBoost as best model at 88%",
            "Built unique energy savings calculator",
            "Added CO2 reduction calculations"
        ]
    },
    {
        "emoji": "🟡",
        "phase": "Phase 4 — Frontend Development",
        "dates": "April 25 - May 8, 2026",
        "color": "#FEF3C7",
        "border": "#F59E0B",
        "tasks": [
            "Built 5 page Streamlit web application",
            "Created Home page with project overview",
            "Created Dashboard with booking analytics",
            "Created Prediction page with ML model",
            "Created Energy Calculator with scenarios",
            "Created Model Evaluation with confusion matrix",
            "Created Development Journey page"
        ]
    },
    {
        "emoji": "🟢",
        "phase": "Phase 5 — Testing",
        "dates": "May 5 - May 12, 2026",
        "color": "#D1FAE5",
        "border": "#10B981",
        "tasks": [
            "Unit tested energy calculator function",
            "Integration tested ML and energy calculator",
            "Validated data cleaning pipeline",
            "Tested all 5 app pages for errors",
            "Fixed NaN value errors in model training"
        ]
    },
    {
        "emoji": "🟡",
        "phase": "Phase 6 — Submission",
        "dates": "May 8 - May 18, 2026",
        "color": "#FEF3C7",
        "border": "#F59E0B",
        "tasks": [
            "Wrote 2300 word technical report",
            "Created Gantt chart for report",
            "Prepared viva presentation guide",
            "Final review of all app pages",
            "Submitted project for assessment"
        ]
    }
]

# Display phases in 2 columns
col1, col2 = st.columns(2)

for i, phase in enumerate(phases):
    card_html = f"""
        <div style='
            background-color: {phase["color"]};
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
            border-left: 5px solid {phase["border"]};
        '>
            <h4 style='color: #064E3B; margin-bottom: 4px;'>
                {phase["emoji"]} {phase["phase"]}
            </h4>
            <p style='color: #444444; font-size: 13px; margin-bottom: 8px;'>
                📅 {phase["dates"]}
            </p>
            {"".join([f"<p style='margin:3px 0; color: #222222;'>✅ {t}</p>" for t in phase["tasks"]])}
        </div>
    """
    if i % 2 == 0:
        with col1:
            st.markdown(card_html, unsafe_allow_html=True)
    else:
        with col2:
            st.markdown(card_html, unsafe_allow_html=True)

st.divider()

# Technologies Used
st.subheader("🛠️ Technologies Used")

tech_col1, tech_col2, tech_col3 = st.columns(3)

with tech_col1:
    st.markdown("""
        <div style='
            background-color: #D1FAE5;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #10B981;
        '>
            <h4 style='color: #064E3B;'>🐍 Data & ML</h4>
            <p style='color: #222222;'>✅ Python 3.x</p>
            <p style='color: #222222;'>✅ Pandas</p>
            <p style='color: #222222;'>✅ NumPy</p>
            <p style='color: #222222;'>✅ Scikit-learn</p>
            <p style='color: #222222;'>✅ XGBoost</p>
        </div>
    """, unsafe_allow_html=True)

with tech_col2:
    st.markdown("""
        <div style='
            background-color: #FEF3C7;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #F59E0B;
        '>
            <h4 style='color: #064E3B;'>📊 Visualization</h4>
            <p style='color: #222222;'>✅ Plotly Express</p>
            <p style='color: #222222;'>✅ Plotly Graph Objects</p>
            <p style='color: #222222;'>✅ Seaborn</p>
            <p style='color: #222222;'>✅ Matplotlib</p>
            <p style='color: #222222;'>✅ Streamlit Charts</p>
        </div>
    """, unsafe_allow_html=True)

with tech_col3:
    st.markdown("""
        <div style='
            background-color: #D1FAE5;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #10B981;
        '>
            <h4 style='color: #064E3B;'>🌐 Development</h4>
            <p style='color: #222222;'>✅ Streamlit</p>
            <p style='color: #222222;'>✅ Jupyter Notebook</p>
            <p style='color: #222222;'>✅ VS Code</p>
            <p style='color: #222222;'>✅ Git</p>
            <p style='color: #222222;'>✅ Pickle</p>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# Footer
st.markdown("""
    <div style='text-align: center; color: #444444;'>
        <p>Hotel Energy Optimizer | Development Journey Page</p>
    </div>
""", unsafe_allow_html=True)