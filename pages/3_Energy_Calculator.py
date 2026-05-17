import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page Config
st.set_page_config(
    page_title="Energy Calculator",
    page_icon="⚡",
    layout="wide"
)

# Title
st.markdown("""
    <h1 style='color: #2E75B6;'>
        ⚡ Hotel Energy Savings Calculator
    </h1>
""", unsafe_allow_html=True)
st.divider()

# Instructions
st.info("""
    👋 Use this calculator to find out exactly 
    how much energy and money your hotel can save 
    based on predicted occupancy levels!
""")

# Energy Calculator Function
def calculate_energy(
    occupancy_rate,
    total_rooms,
    energy_per_room,
    cost_per_kwh,
    days
):
    occupied = round(
        total_rooms * occupancy_rate / 100
    )
    empty = total_rooms - occupied
    energy_saved = empty * energy_per_room * days
    money_saved = round(
        energy_saved * cost_per_kwh, 2
    )
    co2_reduced = round(
        energy_saved * 0.233, 2
    )
    return {
        'occupied': occupied,
        'empty': empty,
        'energy_saved': energy_saved,
        'money_saved': money_saved,
        'co2_reduced': co2_reduced
    }

st.divider()

# Calculator Inputs
st.subheader("🏨 Enter Your Hotel Details")

input_col1, input_col2 = st.columns(2)

with input_col1:
    total_rooms = st.number_input(
        "🏠 Total Number of Rooms",
        min_value=10,
        max_value=1000,
        value=100
    )

    occupancy_rate = st.slider(
        "📊 Predicted Occupancy Rate (%)",
        min_value=0,
        max_value=100,
        value=65
    )

    days = st.slider(
        "📅 Number of Days to Calculate",
        min_value=1,
        max_value=365,
        value=30
    )

with input_col2:
    energy_per_room = st.number_input(
        "⚡ Energy Per Empty Room Per Night (KWh)",
        min_value=10,
        max_value=200,
        value=50
    )

    cost_per_kwh = st.number_input(
        "💰 Cost Per KWh ($)",
        min_value=0.01,
        max_value=1.0,
        value=0.12,
        step=0.01
    )

    hotel_name = st.text_input(
        "🏨 Your Hotel Name",
        value="My Hotel"
    )

st.divider()

# Calculate Button
if st.button(
    "⚡ Calculate Energy Savings!",
    use_container_width=True,
    type="primary"
):
    result = calculate_energy(
        occupancy_rate,
        total_rooms,
        energy_per_room,
        cost_per_kwh,
        days
    )

    st.subheader(
        f"🎯 Results for {hotel_name}"
    )

    # Top Metrics
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric(
            "🛏️ Occupied Rooms",
            f"{result['occupied']}"
        )
    with m2:
        st.metric(
            "🚪 Empty Rooms",
            f"{result['empty']}"
        )
    with m3:
        st.metric(
            "⚡ Energy Saved",
            f"{result['energy_saved']} KWh"
        )
    with m4:
        st.metric(
            "💰 Money Saved",
            f"${result['money_saved']}"
        )

    st.divider()

    # CO2 Result
    st.success(f"""
        ## 🌱 Environmental Impact
        By optimizing energy in empty rooms,
        **{hotel_name}** will reduce CO2 emissions 
        by **{result['co2_reduced']} Kg** 
        over **{days} days!**
    """)

    st.divider()

    # Monthly Breakdown Chart
    st.subheader(
        "📊 Energy Savings Breakdown"
    )

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        # Rooms Pie Chart
        fig1 = px.pie(
            values=[
                result['occupied'],
                result['empty']
            ],
            names=[
                'Occupied Rooms',
                'Empty Rooms'
            ],
            title='Room Occupancy Distribution',
            color_discrete_sequence=[
                '#2ecc71', '#e74c3c'
            ]
        )
        fig1.update_layout(height=350)
        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    with chart_col2:
        # Savings Bar Chart
        savings_data = pd.DataFrame({
            'Category': [
                'Energy (KWh)',
                'Money ($)',
                'CO2 (Kg)'
            ],
            'Value': [
                result['energy_saved'],
                result['money_saved'],
                result['co2_reduced']
            ]
        })

        fig2 = px.bar(
            savings_data,
            x='Category',
            y='Value',
            title='Total Savings Summary',
            color='Category',
            color_discrete_sequence=[
                '#3498db',
                '#2ecc71',
                '#e74c3c'
            ],
            text='Value'
        )
        fig2.update_traces(
            texttemplate='%{text:.1f}',
            textposition='outside'
        )
        fig2.update_layout(height=350)
        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    st.divider()

    # Occupancy Scenarios
    st.subheader(
        "🎯 What If Different Occupancy Rates?"
    )

    scenarios = []
    for rate in range(10, 100, 10):
        r = calculate_energy(
            rate,
            total_rooms,
            energy_per_room,
            cost_per_kwh,
            days
        )
        scenarios.append({
            'Occupancy Rate %': rate,
            'Empty Rooms': r['empty'],
            'Energy Saved KWh': r['energy_saved'],
            'Money Saved $': r['money_saved'],
            'CO2 Reduced Kg': r['co2_reduced']
        })

    scenario_df = pd.DataFrame(scenarios)

    # Scenario Charts
    fig3 = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=(
            '💰 Money Saved vs Occupancy Rate',
            '🌱 CO2 Reduced vs Occupancy Rate'
        )
    )

    fig3.add_trace(
        go.Scatter(
            x=scenario_df['Occupancy Rate %'],
            y=scenario_df['Money Saved $'],
            mode='lines+markers',
            marker_color='#2ecc71',
            name='Money Saved'
        ),
        row=1, col=1
    )

    fig3.add_trace(
        go.Scatter(
            x=scenario_df['Occupancy Rate %'],
            y=scenario_df['CO2 Reduced Kg'],
            mode='lines+markers',
            marker_color='#e74c3c',
            name='CO2 Reduced'
        ),
        row=1, col=2
    )

    fig3.update_layout(height=400)
    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    # Scenario Table
    st.subheader("📋 Full Scenario Table")
    st.dataframe(
        scenario_df,
        use_container_width=True
    )

    st.divider()

    # Download Results
    st.subheader("📥 Download Your Results")
    csv = scenario_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Results as CSV",
        data=csv,
        file_name=f"{hotel_name}_energy_savings.csv",
        mime="text/csv",
        use_container_width=True
    )

st.divider()

# Footer
st.markdown("""
    <div style='text-align: center; 
    color: #666666;'>
        <p>Hotel Energy Optimizer | 
        Energy Calculator Page</p>
    </div>
""", unsafe_allow_html=True)