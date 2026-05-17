import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)
from xgboost import XGBClassifier

# Page Config
st.set_page_config(
    page_title="Model Evaluation",
    page_icon="📈",
    layout="wide"
)

# Title
st.markdown("""
    <h1 style='color: #2E75B6;'>
        📈 Algorithmic Integrity & Evaluation
    </h1>
""", unsafe_allow_html=True)
st.divider()

# Instructions
st.info("""
    👋 This page shows how well our machine 
    learning models perform at predicting 
    hotel booking cancellations!
""")

# Load and Prepare Data
@st.cache_data
def load_and_prepare():
    df = pd.read_csv('hotel_bookings.csv')

    # Fix ALL missing values first
    df['children'] = df['children'].fillna(0)
    df['country'] = df['country'].fillna('Unknown')
    df['agent'] = df['agent'].fillna(0)
    df['company'] = df['company'].fillna(0)

    # Fix ALL other NaN values
    df = df.fillna(0)

    # Remove invalid bookings
    df = df[~(
        (df['adults'] == 0) &
        (df['children'] == 0) &
        (df['babies'] == 0)
    )]

    # Remove invalid ADR
    df = df[df['adr'] >= 0]
    df = df[df['adr'] <= 5000]

    # Feature Engineering
    df['total_guests'] = (
        df['adults'] +
        df['children'] +
        df['babies']
    )
    df['total_nights'] = (
        df['stays_in_weekend_nights'] +
        df['stays_in_week_nights']
    )

    # Remove zero nights
    df = df[df['total_nights'] > 0]

    # Season Function
    def get_season(month):
        if month in [
            'December', 'January', 'February'
        ]:
            return 'Winter'
        elif month in ['March', 'April', 'May']:
            return 'Spring'
        elif month in ['June', 'July', 'August']:
            return 'Summer'
        else:
            return 'Autumn'

    # Lead Time Category Function
    def get_lead_cat(days):
        if days <= 7:
            return 'Last Minute'
        elif days <= 30:
            return 'Short Term'
        elif days <= 90:
            return 'Medium Term'
        else:
            return 'Long Term'

    df['season'] = df[
        'arrival_date_month'
    ].apply(get_season)

    df['lead_time_category'] = df[
        'lead_time'
    ].apply(get_lead_cat)

    # Select Features
    features = [
        'lead_time',
        'total_guests',
        'total_nights',
        'adr',
        'is_repeated_guest',
        'previous_cancellations',
        'previous_bookings_not_canceled',
        'booking_changes',
        'deposit_type',
        'days_in_waiting_list',
        'customer_type',
        'hotel',
        'season',
        'lead_time_category'
    ]

    target = 'is_canceled'

    # Encode text columns
    le = LabelEncoder()
    text_cols = [
        'deposit_type',
        'customer_type',
        'hotel',
        'season',
        'lead_time_category'
    ]

    ml_df = df[features + [target]].copy()

    for col in text_cols:
        ml_df[col] = le.fit_transform(
            ml_df[col].astype(str)
        )

    # Convert all to numeric
    ml_df = ml_df.apply(
        pd.to_numeric, errors='coerce'
    )

    # Drop any remaining NaN
    ml_df = ml_df.dropna()

    X = ml_df[features]
    y = ml_df[target]

    # Split data
    X_train, X_test, y_train, y_test = (
        train_test_split(
            X, y,
            test_size=0.2,
            random_state=42
        )
    )

    return X_train, X_test, y_train, y_test

# Loading Message
with st.spinner(
    "🔄 Training models... Please wait 1-2 minutes..."
):
    try:
        X_train, X_test, y_train, y_test = (
            load_and_prepare()
        )

        # Train Model 1 - Logistic Regression
        lr = LogisticRegression(
            max_iter=1000,
            solver='lbfgs'
        )
        lr.fit(X_train, y_train)
        lr_pred = lr.predict(X_test)
        lr_acc = accuracy_score(y_test, lr_pred)

        # Train Model 2 - Random Forest
        rf = RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )
        rf.fit(X_train, y_train)
        rf_pred = rf.predict(X_test)
        rf_acc = accuracy_score(y_test, rf_pred)

        # Train Model 3 - XGBoost
        xgb = XGBClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42,
            eval_metric='logloss'
        )
        xgb.fit(X_train, y_train)
        xgb_pred = xgb.predict(X_test)
        xgb_acc = accuracy_score(
            y_test, xgb_pred
        )

        st.success(
            "✅ All 3 Models Trained Successfully!"
        )

    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.stop()

st.divider()

# Model Accuracy Metrics
st.subheader("🏆 Model Accuracy Comparison")

m1, m2, m3 = st.columns(3)

with m1:
    st.metric(
        "Logistic Regression",
        f"{round(lr_acc*100, 2)}%"
    )
with m2:
    st.metric(
        "Random Forest",
        f"{round(rf_acc*100, 2)}%"
    )
with m3:
    st.metric(
        "XGBoost",
        f"{round(xgb_acc*100, 2)}%"
    )

st.divider()

# Model Comparison Chart
st.subheader("📊 Model Accuracy Chart")

comparison_df = pd.DataFrame({
    'Model': [
        'Logistic Regression',
        'Random Forest',
        'XGBoost'
    ],
    'Accuracy': [
        round(lr_acc*100, 2),
        round(rf_acc*100, 2),
        round(xgb_acc*100, 2)
    ]
})

fig1 = px.bar(
    comparison_df,
    x='Model',
    y='Accuracy',
    color='Model',
    color_discrete_sequence=[
        '#3498db',
        '#2ecc71',
        '#e74c3c'
    ],
    text='Accuracy',
    title='Model Accuracy Comparison (%)'
)
fig1.update_traces(
    texttemplate='%{text}%',
    textposition='outside'
)
fig1.update_layout(height=400)
st.plotly_chart(
    fig1,
    use_container_width=True
)

st.divider()

# Confusion Matrix
st.subheader(
    "🔢 Confusion Matrix (XGBoost)"
)

cm = confusion_matrix(y_test, xgb_pred)
fig2 = px.imshow(
    cm,
    labels=dict(
        x="Predicted",
        y="Actual",
        color="Count"
    ),
    x=['Not Cancelled', 'Cancelled'],
    y=['Not Cancelled', 'Cancelled'],
    color_continuous_scale='Blues',
    text_auto=True,
    title='XGBoost Confusion Matrix'
)
fig2.update_layout(height=400)
st.plotly_chart(
    fig2,
    use_container_width=True
)

st.divider()

# Classification Report
st.subheader("📋 Classification Report")

report = classification_report(
    y_test,
    xgb_pred,
    output_dict=True
)
report_df = pd.DataFrame(
    report
).transpose().round(3)

st.dataframe(
    report_df,
    use_container_width=True
)

st.divider()

# Feature Importance
st.subheader("🎯 Feature Importance")

features_list = [
    'lead_time',
    'total_guests',
    'total_nights',
    'adr',
    'is_repeated_guest',
    'previous_cancellations',
    'previous_bookings_not_canceled',
    'booking_changes',
    'deposit_type',
    'days_in_waiting_list',
    'customer_type',
    'hotel',
    'season',
    'lead_time_category'
]

importance_df = pd.DataFrame({
    'Feature': features_list,
    'Importance': rf.feature_importances_
}).sort_values(
    'Importance',
    ascending=True
)

fig3 = px.bar(
    importance_df,
    x='Importance',
    y='Feature',
    orientation='h',
    title='Feature Importance - Random Forest',
    color='Importance',
    color_continuous_scale='Reds'
)
fig3.update_layout(height=500)
st.plotly_chart(
    fig3,
    use_container_width=True
)

st.divider()

# Best Model Summary
best_acc = max(lr_acc, rf_acc, xgb_acc)
if best_acc == xgb_acc:
    best_name = "XGBoost"
elif best_acc == rf_acc:
    best_name = "Random Forest"
else:
    best_name = "Logistic Regression"

st.success(f"""
    ## 🏆 Best Model: {best_name}
    
    Accuracy: **{round(best_acc*100, 2)}%**
    
    This model is used for all predictions 
    in this application!
""")

st.divider()

# Footer
st.markdown("""
    <div style='text-align: center; 
    color: #666666;'>
        <p>Hotel Energy Optimizer | 
        Model Evaluation Page</p>
    </div>
""", unsafe_allow_html=True)