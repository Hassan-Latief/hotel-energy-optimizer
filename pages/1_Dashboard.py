import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.markdown("""
    <h1 style='color: #2E75B6;'>
        📊 Hotel Booking Dashboard
    </h1>
""", unsafe_allow_html=True)
st.divider()

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('hotel_bookings.csv')

    # Clean data
    df['children'].fillna(0, inplace=True)
    df['country'].fillna('Unknown', inplace=True)
    df['agent'].fillna(0, inplace=True)
    df['company'].fillna(0, inplace=True)

    # Remove invalid bookings
    df = df[~(
        (df['adults'] == 0) &
        (df['children'] == 0) &
        (df['babies'] == 0)
    )]

    # Remove outliers in ADR
    df = df[df['adr'] >= 0]
    df = df[df['adr'] <= 5000]

    # Fix all remaining NaN
    df = df.fillna(0)

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

    # Season Column
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

    df['season'] = df[
        'arrival_date_month'
    ].apply(get_season)

    # Revenue Lost Column
    df['revenue_lost'] = (
        df['adr'] *
        df['total_nights'] *
        df['is_canceled']
    )

    return df

df = load_data()

# ── CLEANING SUMMARY BOX ──
st.markdown("""
    <div style='
        background-color: #D5F5E3;
        padding: 18px;
        border-radius: 10px;
        border-left: 6px solid #1E8449;
        margin-bottom: 15px;
    '>
        <h4 style='color: #1A1A1A;
        margin-bottom: 5px;'>
            🧹 Data Cleaning Summary
        </h4>
        <p style='color: #1A1A1A; margin: 3px 0;'>
            ✅ Missing values handled in:
            children, country, agent, company
        </p>
        <p style='color: #1A1A1A; margin: 3px 0;'>
            ✅ Invalid bookings removed
            (zero guests)
        </p>
        <p style='color: #1A1A1A; margin: 3px 0;'>
            ✅ ADR outliers removed
            (negative and above 5000)
        </p>
        <p style='color: #1A1A1A; margin: 3px 0;'>
            ✅ 8 new features engineered:
            total_guests, total_nights,
            season, revenue_lost and more
        </p>
        <p style='color: #1A1A1A; margin: 3px 0;'>
            ✅ All remaining NaN values
            filled with zero
        </p>
    </div>
""", unsafe_allow_html=True)

st.divider()

# ── TOP METRICS ──
st.subheader("📈 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

total_bookings = len(df)
cancelled = df['is_canceled'].sum()
cancellation_rate = round(
    cancelled / total_bookings * 100, 2
)
avg_adr = round(df['adr'].mean(), 2)

with col1:
    st.metric(
        "Total Bookings",
        f"{total_bookings:,}"
    )
with col2:
    st.metric(
        "Total Cancellations",
        f"{cancelled:,}"
    )
with col3:
    st.metric(
        "Cancellation Rate",
        f"{cancellation_rate}%"
    )
with col4:
    st.metric(
        "Avg Daily Rate",
        f"${avg_adr}"
    )

st.divider()

# ── MONTH ORDER ──
month_order = [
    'January', 'February', 'March', 'April',
    'May', 'June', 'July', 'August',
    'September', 'October', 'November',
    'December'
]

# ── ROW 1 - TWO CHARTS ──
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("📅 Bookings Per Month")
    monthly = df.groupby(
        'arrival_date_month'
    )['is_canceled'].count().reset_index()
    monthly.columns = ['Month', 'Bookings']
    monthly['Month'] = pd.Categorical(
        monthly['Month'],
        categories=month_order,
        ordered=True
    )
    monthly = monthly.sort_values('Month')
    fig1 = px.bar(
        monthly,
        x='Month',
        y='Bookings',
        color='Bookings',
        color_continuous_scale='Blues'
    )
    fig1.update_layout(height=350)
    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with row1_col2:
    st.subheader("🥧 Cancellation Rate")
    cancel_data = df[
        'is_canceled'
    ].value_counts()
    fig2 = px.pie(
        values=cancel_data.values,
        names=['Not Cancelled', 'Cancelled'],
        color_discrete_sequence=[
            '#2ecc71', '#e74c3c'
        ]
    )
    fig2.update_layout(height=350)
    st.plotly_chart(
        fig2,
        use_container_width=True
    )

st.divider()

# ── ROW 2 - TWO CHARTS ──
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader("🏨 Cancellation by Hotel Type")
    hotel_data = df.groupby('hotel').agg(
        total=('is_canceled', 'count'),
        cancelled=('is_canceled', 'sum')
    ).reset_index()
    hotel_data['rate'] = round(
        hotel_data['cancelled'] /
        hotel_data['total'] * 100, 2
    )
    fig3 = px.bar(
        hotel_data,
        x='hotel',
        y='rate',
        color='hotel',
        color_discrete_sequence=[
            '#3498db', '#e67e22'
        ],
        labels={'rate': 'Cancellation Rate %'}
    )
    fig3.update_layout(height=350)
    st.plotly_chart(
        fig3,
        use_container_width=True
    )

with row2_col2:
    st.subheader("🌍 Bookings by Season")
    season_data = df.groupby(
        'season'
    )['is_canceled'].count().reset_index()
    season_data.columns = ['Season', 'Bookings']
    fig4 = px.bar(
        season_data,
        x='Season',
        y='Bookings',
        color='Season',
        color_discrete_sequence=[
            '#3498db', '#2ecc71',
            '#e74c3c', '#f39c12'
        ]
    )
    fig4.update_layout(height=350)
    st.plotly_chart(
        fig4,
        use_container_width=True
    )

st.divider()

# ── ROW 3 - HEATMAP ──
st.subheader(
    "🔥 Cancellation Heatmap by Month and Hotel"
)
pivot = df.groupby(
    ['arrival_date_month', 'hotel']
)['is_canceled'].mean().unstack()
pivot = pivot.reindex(month_order)

fig5 = px.imshow(
    pivot,
    color_continuous_scale='RdYlGn_r',
    aspect='auto',
    title='Cancellation Rate by Month and Hotel Type'
)
fig5.update_layout(height=450)
st.plotly_chart(fig5, use_container_width=True)

st.divider()

# ── ROW 4 - REVENUE LOST ──
st.subheader("💸 Revenue Lost by Month")
revenue_month = df.groupby(
    'arrival_date_month'
)['revenue_lost'].sum().reset_index()
revenue_month.columns = ['Month', 'Revenue Lost']
revenue_month['Month'] = pd.Categorical(
    revenue_month['Month'],
    categories=month_order,
    ordered=True
)
revenue_month = revenue_month.sort_values('Month')

fig6 = px.area(
    revenue_month,
    x='Month',
    y='Revenue Lost',
    title='Revenue Lost Due to Cancellations',
    color_discrete_sequence=['#e74c3c']
)
fig6.update_layout(height=380)
st.plotly_chart(fig6, use_container_width=True)

st.divider()

# ── DOWNLOAD CLEANED DATASETS ──
st.subheader("📥 Download Cleaned Datasets")

st.markdown("""
    <div style='
        background-color: #D6EAF8;
        padding: 15px;
        border-radius: 10px;
        border-left: 6px solid #2980B9;
        margin-bottom: 15px;
    '>
        <p style='color: #1A1A1A; margin: 0;'>
            ℹ️ These are the cleaned versions
            of both datasets after all missing
            values, outliers, and invalid records
            have been removed and new features
            have been added.
        </p>
    </div>
""", unsafe_allow_html=True)

dl1, dl2 = st.columns(2)

with dl1:
    st.markdown("""
        <div style='
            background-color: #EAFAF1;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #1E8449;
            margin-bottom: 10px;
        '>
            <h4 style='color: #1A1A1A;'>
                🏨 Hotel Booking Dataset
            </h4>
            <p style='color: #333333;
            margin: 3px 0;'>
                ✅ Missing values handled
            </p>
            <p style='color: #333333;
            margin: 3px 0;'>
                ✅ Invalid bookings removed
            </p>
            <p style='color: #333333;
            margin: 3px 0;'>
                ✅ Outliers removed
            </p>
            <p style='color: #333333;
            margin: 3px 0;'>
                ✅ New features added
            </p>
            <p style='color: #1E8449;
            font-weight: bold;'>
                Rows: {rows:,} |
                Columns: {cols}
            </p>
        </div>
    """.format(
        rows=len(df),
        cols=len(df.columns)
    ), unsafe_allow_html=True)

    csv1 = df.to_csv(index=False)
    st.download_button(
        label="📥 Download Cleaned Hotel Dataset",
        data=csv1,
        file_name="hotel_bookings_cleaned.csv",
        mime="text/csv",
        use_container_width=True
    )

with dl2:
    try:
        energy_df = pd.read_excel(
            'ENB2012_data.xlsx'
        )
        energy_df.columns = [
            'Relative_Compactness',
            'Surface_Area',
            'Wall_Area',
            'Roof_Area',
            'Overall_Height',
            'Orientation',
            'Glazing_Area',
            'Glazing_Distribution',
            'Heating_Load',
            'Cooling_Load'
        ]
        energy_df = energy_df.fillna(0)

        st.markdown("""
            <div style='
                background-color: #EBF5FB;
                padding: 15px;
                border-radius: 10px;
                border-left: 5px solid #2980B9;
                margin-bottom: 10px;
            '>
                <h4 style='color: #1A1A1A;'>
                    ⚡ Energy Efficiency Dataset
                </h4>
                <p style='color: #333333;
                margin: 3px 0;'>
                    ✅ Columns renamed clearly
                </p>
                <p style='color: #333333;
                margin: 3px 0;'>
                    ✅ Missing values handled
                </p>
                <p style='color: #333333;
                margin: 3px 0;'>
                    ✅ Ready for ML models
                </p>
                <p style='color: #333333;
                margin: 3px 0;'>
                    ✅ Heating and Cooling loads
                </p>
                <p style='color: #2980B9;
                font-weight: bold;'>
                    Rows: {rows:,} |
                    Columns: {cols}
                </p>
            </div>
        """.format(
            rows=len(energy_df),
            cols=len(energy_df.columns)
        ), unsafe_allow_html=True)

        csv2 = energy_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Cleaned Energy Dataset",
            data=csv2,
            file_name="energy_efficiency_cleaned.csv",
            mime="text/csv",
            use_container_width=True
        )

    except Exception as e:
        st.warning(
            "Energy dataset file not found. "
            "Make sure ENB2012_data.xlsx is "
            "in your project folder."
        )

st.divider()

# ── FOOTER ──
st.markdown("""
    <div style='
        text-align: center;
        color: #666666;
    '>
        <p>Hotel Energy Optimizer |
        Dashboard Page</p>
    </div>
""", unsafe_allow_html=True)