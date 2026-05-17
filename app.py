from download_data import download_hotel_data
from train_model import train_and_save_model

download_hotel_data()
train_and_save_model()

import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Hotel Energy Optimizer",
    page_icon="🏨",
    layout="wide"
)

# Custom CSS for better design
st.markdown("""
    <style>
        .main {
            background-color: #F0FAF4;
        }
        .stMetric {
            background-color: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.08);
        }
    </style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
    <div style='
        background: linear-gradient(135deg, #064E3B 0%, #10B981 100%);
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
    '>
        <h1 style='color: white; font-size: 3em; margin-bottom: 5px;'>
            🏨 Hotel Energy Optimizer
        </h1>
        <h3 style='color: #A7F3D0; font-weight: normal;'>
            Energy Efficiency Optimization using 
            Hotel Booking Demand Prediction
        </h3>
        <p style='color: #6EE7B7; font-size: 16px;'>
            Powered by Random Forest Machine Learning | 
            119,390 Real Booking Records
        </p>
    </div>
""", unsafe_allow_html=True)

# ── Project At A Glance ──────────────────────────────────────────
st.subheader("📊 Project At A Glance")

c1, c2, c3, c4, c5, c6 = st.columns(6)

metric_style = """
    background: linear-gradient(135deg, {bg1}, {bg2});
    padding: 18px 12px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 2px 4px 12px rgba(0,0,0,0.15);
    height: 110px;
    display: flex;
    flex-direction: column;
    justify-content: center;
"""

metrics = [
    (c1, "📁", "Total Records", "119,390",  "#064E3B", "#10B981"),
    (c2, "❌", "Cancel Rate",   "37%",       "#7F1D1D", "#EF4444"),
    (c3, "🤖", "ML Models",    "3",          "#1E3A5F", "#3B82F6"),
    (c4, "🎯", "Best Accuracy","81.28%",     "#3B0764", "#8B5CF6"),
    (c5, "⚡", "Energy/Room",  "50 KWh",    "#78350F", "#F59E0B"),
    (c6, "📄", "App Pages",    "7",          "#064E3B", "#34D399"),
]

for col, icon, label, value, bg1, bg2 in metrics:
    with col:
        st.markdown(f"""
            <div style='{metric_style.format(bg1=bg1, bg2=bg2)}'>
                <div style='font-size: 22px;'>{icon}</div>
                <div style='color: #FFFFFF; font-size: 22px; font-weight: 700;
                            line-height: 1.2;'>{value}</div>
                <div style='color: #E2E8F0; font-size: 11px;
                            margin-top: 2px;'>{label}</div>
            </div>
        """, unsafe_allow_html=True)

st.divider()

# ── Project Overview + Datasets ──────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div style='
            background-color: #064E3B;
            padding: 25px;
            border-radius: 12px;
            border-left: 6px solid #10B981;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.08);
            height: 100%;
        '>
            <h3 style='color: #A7F3D0;'>📋 Project Overview</h3>
            <p style='color: #FFFFFF; line-height: 1.8;'>
                Hotel Energy Optimizer is an intelligent 
                decision support system that helps hotel 
                managers reduce energy consumption by 
                predicting which bookings will be cancelled.
            </p>
            <p style='color: #FFFFFF; line-height: 1.8;'>
                Empty rooms waste energy through unnecessary 
                heating, cooling and lighting. By predicting 
                cancellations accurately, hotels can switch 
                off energy in empty rooms proactively saving 
                money and reducing carbon emissions.
            </p>
            <p style='color: #FFFFFF; line-height: 1.8;'>
                The system uses three machine learning models 
                and selects the best performing Random Forest 
                model which achieved 81.28% accuracy on the 
                hotel booking dataset.
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style='
            background-color: #1C1C2E;
            padding: 25px;
            border-radius: 12px;
            border-left: 6px solid #F59E0B;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.08);
        '>
            <h3 style='color: #FCD34D;'>📦 Datasets Used</h3>
            <div style='
                background: #065F46;
                padding: 12px;
                border-radius: 8px;
                margin-bottom: 12px;
            '>
                <b style='color: #6EE7B7;'>
                    🏨 Hotel Booking Demand
                </b><br>
                <small style='color: #A7F3D0;'>
                    Source: Kaggle (Open Source)
                </small><br>
                <span style='color: #FFFFFF;'>
                    ✅ 119,390 booking records
                </span><br>
                <span style='color: #FFFFFF;'>
                    ✅ 32 features
                </span><br>
                <span style='color: #FFFFFF;'>
                    ✅ 2015 - 2017 data
                </span><br>
                <span style='color: #FFFFFF;'>
                    ✅ City and Resort hotels
                </span>
            </div>
            <div style='
                background: #78350F;
                padding: 12px;
                border-radius: 8px;
            '>
                <b style='color: #FCD34D;'>
                    ⚡ Energy Efficiency Dataset
                </b><br>
                <small style='color: #FDE68A;'>
                    Source: UCI Machine Learning Repository
                </small><br>
                <span style='color: #FFFFFF;'>
                    ✅ 768 building records
                </span><br>
                <span style='color: #FFFFFF;'>
                    ✅ 10 energy features
                </span><br>
                <span style='color: #FFFFFF;'>
                    ✅ Heating and cooling loads
                </span><br>
                <span style='color: #FFFFFF;'>
                    ✅ Building characteristics
                </span>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# ── How To Use ───────────────────────────────────────────────────
st.subheader("🗺️ How To Use This App")

s1, s2, s3, s4, s5 = st.columns(5)

with s1:
    st.markdown("""
        <div style='
            background: linear-gradient(
                135deg, #10B981, #059669
            );
            padding: 20px; border-radius: 12px;
            text-align: center; color: white;
            height: 180px;
        '>
            <h2>📊</h2>
            <b>Step 1</b><br>Dashboard<br>
            <small>View booking trends
            and patterns</small>
        </div>
    """, unsafe_allow_html=True)

with s2:
    st.markdown("""
        <div style='
            background: linear-gradient(
                135deg, #F59E0B, #D97706
            );
            padding: 20px; border-radius: 12px;
            text-align: center; color: white;
            height: 180px;
        '>
            <h2>🤖</h2>
            <b>Step 2</b><br>Prediction<br>
            <small>Predict booking
            cancellation risk</small>
        </div>
    """, unsafe_allow_html=True)

with s3:
    st.markdown("""
        <div style='
            background: linear-gradient(
                135deg, #064E3B, #065F46
            );
            padding: 20px; border-radius: 12px;
            text-align: center; color: white;
            height: 180px;
        '>
            <h2>⚡</h2>
            <b>Step 3</b><br>Energy Calculator<br>
            <small>Calculate energy
            and money savings</small>
        </div>
    """, unsafe_allow_html=True)

with s4:
    st.markdown("""
        <div style='
            background: linear-gradient(
                135deg, #34D399, #10B981
            );
            padding: 20px; border-radius: 12px;
            text-align: center; color: white;
            height: 180px;
        '>
            <h2>📈</h2>
            <b>Step 4</b><br>Model Evaluation<br>
            <small>View model accuracy
            and comparison</small>
        </div>
    """, unsafe_allow_html=True)

with s5:
    st.markdown("""
        <div style='
            background: linear-gradient(
                135deg, #FBBF24, #F59E0B
            );
            padding: 20px; border-radius: 12px;
            text-align: center; color: white;
            height: 180px;
        '>
            <h2>🗺️</h2>
            <b>Step 5</b><br>Dev Journey<br>
            <small>View project
            development timeline</small>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# ── Key Features ─────────────────────────────────────────────────
st.subheader("🌟 Key Features")

f1, f2, f3 = st.columns(3)

with f1:
    st.markdown("""
        <div style='
            background: linear-gradient(
                135deg, #065F46, #10B981
            );
            padding: 22px; border-radius: 12px;
            box-shadow: 2px 4px 12px rgba(0,0,0,0.15);
        '>
            <h4 style='color: #A7F3D0; margin-top: 0;'>
                🤖 Advanced ML Models
            </h4>
            <p style='color: #FFFFFF;
            line-height: 1.7; margin: 0;'>
                Three models trained and compared:
                Logistic Regression, Random Forest
                and XGBoost. Random Forest selected
                as best model with 81.28% accuracy.
            </p>
        </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown("""
        <div style='
            background: linear-gradient(
                135deg, #1E3A5F, #3B82F6
            );
            padding: 22px; border-radius: 12px;
            box-shadow: 2px 4px 12px rgba(0,0,0,0.15);
        '>
            <h4 style='color: #BFDBFE; margin-top: 0;'>
                ⚡ Energy Calculator
            </h4>
            <p style='color: #FFFFFF;
            line-height: 1.7; margin: 0;'>
                Unique feature that converts ML
                predictions into real energy savings
                in KWh, money saved in dollars and
                CO2 reduction in kilograms.
            </p>
        </div>
    """, unsafe_allow_html=True)

with f3:
    st.markdown("""
        <div style='
            background: linear-gradient(
                135deg, #78350F, #F59E0B
            );
            padding: 22px; border-radius: 12px;
            box-shadow: 2px 4px 12px rgba(0,0,0,0.15);
        '>
            <h4 style='color: #FDE68A; margin-top: 0;'>
                📊 Interactive Dashboard
            </h4>
            <p style='color: #FFFFFF;
            line-height: 1.7; margin: 0;'>
                15+ professional interactive charts
                including heatmaps, bar charts, pie
                charts, scatter plots and a complete
                energy efficiency dashboard.
            </p>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# ── Footer ───────────────────────────────────────────────────────
st.markdown("""
    <div style='
        background: linear-gradient(
            135deg, #064E3B 0%, #10B981 100%
        );
        padding: 20px; border-radius: 10px;
        text-align: center;
    '>
        <p style='color: white; margin: 0;'>
            🏨 Hotel Energy Optimizer |
            Energy Efficiency Optimization
            using Hotel Booking Demand Prediction
        </p>
        <p style='color: #A7F3D0; font-size: 13px;
        margin: 5px 0 0 0;'>
            Dataset: Hotel Booking Demand (Kaggle) |
            UCI Energy Efficiency |
            Built with Python and Streamlit
        </p>
    </div>
""", unsafe_allow_html=True)
