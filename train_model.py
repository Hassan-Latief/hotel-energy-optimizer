import pandas as pd
import pickle
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def train_and_save_model():
    if os.path.exists('best_model.pkl'):
        print("Model already exists!")
        return

    print("Training Random Forest model...")

    # Load data
    df = pd.read_csv('hotel_bookings.csv')

    # Clean
    df['children'].fillna(0, inplace=True)
    df['country'].fillna('Unknown', inplace=True)
    df['agent'].fillna(0, inplace=True)
    df['company'].fillna(0, inplace=True)
    df = df.fillna(0)

    df = df[~(
        (df['adults'] == 0) &
        (df['children'] == 0) &
        (df['babies'] == 0)
    )]

    df = df[df['adr'] >= 0]
    df = df[df['adr'] <= 5000]

    # Features
    df['total_guests'] = (
        df['adults'] +
        df['children'] +
        df['babies']
    )
    df['total_nights'] = (
        df['stays_in_weekend_nights'] +
        df['stays_in_week_nights']
    )
    df = df[df['total_nights'] > 0]

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

    features = [
        'lead_time', 'total_guests',
        'total_nights', 'adr',
        'is_repeated_guest',
        'previous_cancellations',
        'previous_bookings_not_canceled',
        'booking_changes', 'deposit_type',
        'days_in_waiting_list',
        'customer_type', 'hotel',
        'season', 'lead_time_category'
    ]

    target = 'is_canceled'
    le = LabelEncoder()
    text_cols = [
        'deposit_type', 'customer_type',
        'hotel', 'season', 'lead_time_category'
    ]

    ml_df = df[features + [target]].copy()
    for col in text_cols:
        ml_df[col] = le.fit_transform(
            ml_df[col].astype(str)
        )

    ml_df = ml_df.apply(
        pd.to_numeric, errors='coerce'
    )
    ml_df = ml_df.dropna()

    X = ml_df[features]
    y = ml_df[target]

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X, y,
            test_size=0.2,
            random_state=42
        )
    )

    # Train Random Forest
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )
    model.fit(X_train, y_train)

    # Save model
    with open('best_model.pkl', 'wb') as f:
        pickle.dump(model, f)

    print("Random Forest trained and saved!")
