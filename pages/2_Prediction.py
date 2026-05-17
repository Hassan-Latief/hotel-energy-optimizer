import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder

# Page Config
st.set_page_config(
    page_title="Prediction",
    page_icon="🤖",
    layout="wide"
)

# Title
st.markdown("""
    <h1 style='color: #2E75B6;'>
        🤖 Booking Cancellation Predictor
    </h1>
""", unsafe_allow_html=True)
st.divider()

# Load Model
@st.cache_resource
def load_model():
    with open('best_model.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

model = load_model()

# Load Data for encoding
@st.cache_data
def load_data():
    df = pd.read_csv('hotel_bookings.csv')
    df['children'].fillna(0, inplace=True)
    df['agent'].fillna(0, inplace=True)
    df['company'].fillna(0, inplace=True)
    return df

df = load_data()

# Instructions
st.info("""
    👋 Fill in the booking details below and
    click Predict to find out if the booking
    will be cancelled or not!

    🤖 Powered by Random Forest Classifier
    with 81.28% accuracy — the best performing
    model in this project.
""")

st.subheader("📋 Enter Booking Details")

# Input Form
col1, col2 = st.columns(2)

with col1:
    hotel = st.selectbox(
        "🏨 Hotel Type",
        ["City Hotel", "Resort Hotel"]
    )

    lead_time = st.slider(
        "📅 Lead Time (Days before arrival)",
        min_value=0,
        max_value=365,
        value=30
    )

    adults = st.number_input(
        "👨 Number of Adults",
        min_value=1,
        max_value=10,
        value=2
    )

    children = st.number_input(
        "👶 Number of Children",
        min_value=0,
        max_value=5,
        value=0
    )

    babies = st.number_input(
        "🍼 Number of Babies",
        min_value=0,
        max_value=5,
        value=0
    )

    weekend_nights = st.slider(
        "🌙 Weekend Nights",
        min_value=0,
        max_value=7,
        value=1
    )

    week_nights = st.slider(
        "📆 Week Nights",
        min_value=0,
        max_value=14,
        value=2
    )

with col2:
    deposit_type = st.selectbox(
        "💳 Deposit Type",
        ["No Deposit", "Non Refund", "Refundable"]
    )

    customer_type = st.selectbox(
        "👥 Customer Type",
        ["Transient", "Contract",
         "Transient-Party", "Group"]
    )

    season = st.selectbox(
        "🌍 Season of Arrival",
        ["Summer", "Winter", "Spring", "Autumn"]
    )

    adr = st.number_input(
        "💰 Average Daily Rate ($)",
        min_value=0,
        max_value=1000,
        value=100
    )

    previous_cancellations = st.number_input(
        "❌ Previous Cancellations",
        min_value=0,
        max_value=20,
        value=0
    )

    previous_bookings = st.number_input(
        "✅ Previous Bookings Not Cancelled",
        min_value=0,
        max_value=50,
        value=0
    )

    booking_changes = st.number_input(
        "🔄 Booking Changes",
        min_value=0,
        max_value=20,
        value=0
    )

    days_waiting = st.number_input(
        "⏳ Days in Waiting List",
        min_value=0,
        max_value=100,
        value=0
    )

st.divider()

# Model Info Box
st.markdown("""
    <div style='
        background-color: #D5F5E3;
        padding: 15px;
        border-radius: 10px;
        border-left: 6px solid #1E8449;
        margin-bottom: 15px;
    '>
        <h4 style='color: #1A1A1A; margin: 0;'>
            🤖 Model Information
        </h4>
        <p style='color: #1A1A1A; margin: 5px 0 0 0;'>
            ✅ Algorithm: Random Forest Classifier
            (Best Model)<br>
            ✅ Accuracy: 81.28% on test set<br>
            ✅ Compared against: Logistic
            Regression (76%) and XGBoost (77.99%)<br>
            ✅ Training data: 119,390 hotel
            booking records
        </p>
    </div>
""", unsafe_allow_html=True)

# Predict Button
if st.button(
    "🔮 Predict Cancellation",
    use_container_width=True,
    type="primary"
):
    # Calculate derived features
    total_guests = adults + children + babies
    total_nights = weekend_nights + week_nights

    # Get lead time category
    if lead_time <= 7:
        lead_cat = "Last Minute"
    elif lead_time <= 30:
        lead_cat = "Short Term"
    elif lead_time <= 90:
        lead_cat = "Medium Term"
    else:
        lead_cat = "Long Term"

    # Encode categorical variables
    le = LabelEncoder()

    # Fit on original data
    hotel_encoded = le.fit(
        df['hotel']
    ).transform([hotel])[0]

    deposit_encoded = le.fit(
        df['deposit_type']
    ).transform([deposit_type])[0]

    customer_encoded = le.fit(
        df['customer_type']
    ).transform([customer_type])[0]

    # Manual encoding for new columns
    season_map = {
        "Summer": 3,
        "Spring": 2,
        "Winter": 4,
        "Autumn": 0
    }
    lead_map = {
        "Last Minute": 1,
        "Short Term": 2,
        "Medium Term": 0,
        "Long Term": 3
    }

    season_encoded = season_map[season]
    lead_encoded = lead_map[lead_cat]

    # Create input array
    input_data = np.array([[
        lead_time,
        total_guests,
        total_nights,
        adr,
        0,  # is_repeated_guest
        previous_cancellations,
        previous_bookings,
        booking_changes,
        deposit_encoded,
        days_waiting,
        customer_encoded,
        hotel_encoded,
        season_encoded,
        lead_encoded
    ]])

    # Make prediction
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(
        input_data
    )[0]

    st.divider()
    st.subheader("🎯 Prediction Result")

    result_col1, result_col2 = st.columns(2)

    with result_col1:
        if prediction == 1:
            st.error("""
                ## ❌ HIGH CANCELLATION RISK!

                This booking is likely to be
                CANCELLED

                Hotel should prepare for
                potential empty room and
                reduce energy usage accordingly
            """)
        else:
            st.success("""
                ## ✅ LOW CANCELLATION RISK!

                This booking is likely to
                PROCEED

                Hotel should prepare the room
                and allocate full energy
                resources
            """)

    with result_col2:
        st.subheader("📊 Prediction Confidence")
        cancel_prob = round(
            probability[1] * 100, 1
        )
        stay_prob = round(
            probability[0] * 100, 1
        )

        st.metric(
            "Cancellation Probability",
            f"{cancel_prob}%"
        )
        st.metric(
            "Stay Probability",
            f"{stay_prob}%"
        )

        # Energy Recommendation
        st.subheader("⚡ Energy Recommendation")
        if prediction == 1:
            st.warning("""
                **Energy Saving Mode**

                - Turn off HVAC in this room
                - Reduce lighting to minimum
                - Estimated saving: 50 KWh
                - Money saved: $6.00
            """)
        else:
            st.info("""
                **Normal Energy Mode**

                - Maintain normal HVAC
                - Keep full lighting
                - Prepare room fully
                - Standard energy usage
            """)

    # Show model used
    st.divider()
    st.markdown("""
        <div style='
            background-color: #EBF5FB;
            padding: 12px;
            border-radius: 8px;
            border-left: 5px solid #2980B9;
        '>
            <p style='color: #1A1A1A; margin: 0;'>
                🤖 Prediction made by:
                <b>Random Forest Classifier</b>
                | Accuracy: <b>81.28%</b>
            </p>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# Footer
st.markdown("""
    <div style='text-align: center;
    color: #666666;'>
        <p>Hotel Energy Optimizer |
        Prediction Page |
        Powered by Random Forest 81.28%</p>
    </div>
""", unsafe_allow_html=True)
