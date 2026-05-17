import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page Config
st.set_page_config(
    page_title="Energy Action Plan",
    page_icon="⚡",
    layout="wide"
)

# Title
st.markdown("""
    <div style='
        background-color: #1F3864;
        padding: 30px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 20px;
    '>
        <h1 style='color: white;'>
            ⚡ AI-Based Energy Decision
            Support System
        </h1>
        <p style='color: #BDE3FF;
        font-size: 17px;'>
            Saving Energy Whether Your Hotel
            is Empty OR Fully Booked
        </p>
    </div>
""", unsafe_allow_html=True)

st.divider()

# KEY MESSAGE BOX
st.markdown("""
    <div style='
        background-color: #D5F5E3;
        padding: 20px;
        border-radius: 10px;
        border-left: 6px solid #1E8449;
        margin-bottom: 20px;
    '>
        <h3 style='color: #1A1A1A;'>
            🎯 Core Idea of This System
        </h3>
        <p style='color: #1A1A1A;
        font-size: 15px; line-height: 1.8;'>
            Traditional energy systems waste
            energy because they run at
            <b>FULL POWER ALL THE TIME</b>
            regardless of actual need.
            <br><br>
            This AI system is different.
            It predicts exactly when, where,
            and how much energy is needed
            and adjusts automatically —
            <b>whether the hotel has
            0% or 100% occupancy.</b>
        </p>
    </div>
""", unsafe_allow_html=True)

st.divider()

# Hotel Inputs
st.subheader("🏨 Enter Your Hotel Details")

col1, col2, col3 = st.columns(3)

with col1:
    total_rooms = st.number_input(
        "Total Rooms",
        min_value=10,
        max_value=500,
        value=100
    )
    total_floors = st.number_input(
        "Total Floors",
        min_value=1,
        max_value=30,
        value=5
    )

with col2:
    predicted_occupancy = st.slider(
        "Predicted Occupancy Rate (%)",
        min_value=0,
        max_value=100,
        value=100
    )
    current_season = st.selectbox(
        "Current Season",
        ["Summer", "Winter",
         "Spring", "Autumn"]
    )

with col3:
    weather_temp = st.slider(
        "Outside Temperature (°C)",
        min_value=-10,
        max_value=45,
        value=28
    )
    time_of_day = st.selectbox(
        "Time of Day",
        [
            "Morning (6AM-12PM)",
            "Afternoon (12PM-6PM)",
            "Evening (6PM-12AM)",
            "Night (12AM-6AM)"
        ]
    )

st.divider()

if st.button(
    "🤖 Generate AI Energy Action Plan",
    use_container_width=True,
    type="primary"
):
    # Core calculations
    occupied_rooms = round(
        total_rooms * predicted_occupancy / 100
    )
    empty_rooms = total_rooms - occupied_rooms
    rooms_per_floor = max(
        1, total_rooms // total_floors
    )
    active_floors = min(
        total_floors,
        (occupied_rooms + rooms_per_floor - 1)
        // rooms_per_floor
    )
    idle_floors = total_floors - active_floors

    # Determine scenario
    is_full = predicted_occupancy >= 90
    is_empty = predicted_occupancy <= 30

    if is_full:
        scenario = "🔴 HIGH OCCUPANCY"
        scenario_color = "#FADBD8"
        scenario_border = "#C0392B"
        scenario_msg = (
            "Hotel is nearly fully booked. "
            "Energy savings come from SMART "
            "USAGE PATTERNS inside occupied rooms."
        )
    elif is_empty:
        scenario = "🟢 LOW OCCUPANCY"
        scenario_color = "#D5F5E3"
        scenario_border = "#1E8449"
        scenario_msg = (
            "Hotel has many empty rooms. "
            "Energy savings come from "
            "SHUTTING DOWN unused areas."
        )
    else:
        scenario = "🟡 MEDIUM OCCUPANCY"
        scenario_color = "#FDEBD0"
        scenario_border = "#D68910"
        scenario_msg = (
            "Hotel is partially booked. "
            "Energy savings come from BOTH "
            "empty room shutdown AND smart "
            "usage patterns."
        )

    # Show scenario
    st.markdown(f"""
        <div style='
            background-color: {scenario_color};
            padding: 18px;
            border-radius: 10px;
            border-left: 6px solid
            {scenario_border};
            margin-bottom: 15px;
        '>
            <h3 style='color: #1A1A1A;'>
                Current Scenario:
                {scenario}
            </h3>
            <p style='color: #222222;
            font-size: 15px;'>
                {scenario_msg}
            </p>
            <p style='color: #222222;'>
                <b>{occupied_rooms}</b> rooms
                occupied |
                <b>{empty_rooms}</b> rooms
                empty |
                <b>{active_floors}</b> floors
                active |
                <b>{idle_floors}</b> floors idle
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── TECHNIQUE 1: SMART HVAC ──
    st.markdown("""
        <div style='
            background-color: #D6EAF8;
            padding: 18px;
            border-radius: 10px;
            border-left: 6px solid #2980B9;
            margin-bottom: 10px;
        '>
            <h3 style='color: #1A1A1A;'>
                1️⃣ Smart HVAC Optimization
            </h3>
        </div>
    """, unsafe_allow_html=True)

    hvac1, hvac2 = st.columns(2)

    with hvac1:
        # Calculate HVAC savings both scenarios
        if is_full:
            # Full hotel - save through smart
            # temperature management
            night_saving = round(
                occupied_rooms * 50 * 0.15, 1
            )
            sleep_saving = round(
                occupied_rooms * 50 * 0.10, 1
            )
            hvac_total = round(
                night_saving + sleep_saving, 1
            )
            st.markdown(f"""
                <div style='
                    background-color: #EBF5FB;
                    padding: 15px;
                    border-radius: 8px;
                '>
                    <p style='color:#1A1A1A;'>
                        <b>Even with 100% occupancy
                        the system saves energy
                        through:</b>
                    </p>
                    <p style='color:#1A1A1A;
                    margin:4px 0;'>
                        ✅ Night mode (12AM-6AM):
                        Reduce AC by 2°C when
                        guests are sleeping →
                        Saves <b>{night_saving}
                        KWh</b>
                    </p>
                    <p style='color:#1A1A1A;
                    margin:4px 0;'>
                        ✅ Smart thermostat:
                        Detect when guest leaves
                        room and reduce AC
                        automatically →
                        Saves <b>{sleep_saving}
                        KWh</b>
                    </p>
                    <p style='color:#1A1A1A;
                    margin:4px 0;'>
                        ✅ Pre-cooling only when
                        needed based on weather
                        ({weather_temp}°C outside)
                    </p>
                    <p style='color:#1A1A1A;
                    margin:4px 0;'>
                        ✅ Corridor and lobby AC
                        reduced during low
                        traffic hours
                    </p>
                    <p style='color:#1E8449;
                    font-weight:bold;
                    margin-top:10px;'>
                        Total HVAC Saving:
                        {hvac_total} KWh
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else:
            hvac_total = round(
                empty_rooms * 50 * 0.35, 1
            )
            st.markdown(f"""
                <div style='
                    background-color: #EBF5FB;
                    padding: 15px;
                    border-radius: 8px;
                '>
                    <p style='color:#1A1A1A;'>
                        <b>With {empty_rooms}
                        empty rooms the system
                        saves energy through:</b>
                    </p>
                    <p style='color:#1A1A1A;
                    margin:4px 0;'>
                        ✅ Empty rooms AC set
                        to standby mode →
                        Saves <b>{round(
                            empty_rooms*50*0.25,1
                        )} KWh</b>
                    </p>
                    <p style='color:#1A1A1A;
                    margin:4px 0;'>
                        ✅ Occupied rooms smart
                        temperature management
                        → Saves <b>{round(
                            occupied_rooms*50*0.10,
                            1
                        )} KWh</b>
                    </p>
                    <p style='color:#1A1A1A;
                    margin:4px 0;'>
                        ✅ Pre-cooling activated
                        based on weather
                        ({weather_temp}°C outside)
                    </p>
                    <p style='color:#1E8449;
                    font-weight:bold;
                    margin-top:10px;'>
                        Total HVAC Saving:
                        {hvac_total} KWh
                    </p>
                </div>
            """, unsafe_allow_html=True)

    with hvac2:
        # HVAC Chart
        if is_full:
            hvac_df = pd.DataFrame({
                'Time Period': [
                    'Day Time',
                    'Evening',
                    'Night Mode',
                    'Early Morning'
                ],
                'Energy Without AI (KWh)': [
                    120, 130, 125, 110
                ],
                'Energy With AI (KWh)': [
                    110, 118, 95, 85
                ]
            })
        else:
            hvac_df = pd.DataFrame({
                'Room Type': [
                    'Occupied Full AC',
                    'Empty Standby',
                    'Corridor/Lobby',
                    'Common Areas'
                ],
                'Energy Without AI (KWh)': [
                    occupied_rooms * 0.5,
                    empty_rooms * 0.5,
                    30, 20
                ],
                'Energy With AI (KWh)': [
                    occupied_rooms * 0.45,
                    empty_rooms * 0.1,
                    20, 15
                ]
            })

        col_name = (
            'Time Period'
            if is_full else 'Room Type'
        )
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            name='Without AI',
            x=hvac_df[col_name],
            y=hvac_df[
                'Energy Without AI (KWh)'
            ],
            marker_color='#E74C3C'
        ))
        fig1.add_trace(go.Bar(
            name='With AI',
            x=hvac_df[col_name],
            y=hvac_df['Energy With AI (KWh)'],
            marker_color='#2ECC71'
        ))
        fig1.update_layout(
            title='HVAC: Before vs After AI',
            barmode='group',
            height=320
        )
        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    st.divider()

    # ── TECHNIQUE 2: FLOOR MANAGEMENT ──
    st.markdown("""
        <div style='
            background-color: #D5F5E3;
            padding: 18px;
            border-radius: 10px;
            border-left: 6px solid #1E8449;
            margin-bottom: 10px;
        '>
            <h3 style='color: #1A1A1A;'>
                2️⃣ Floor-Wise Energy Management
            </h3>
        </div>
    """, unsafe_allow_html=True)

    fl1, fl2 = st.columns(2)

    with fl1:
        floor_rows = []
        for floor in range(1, total_floors + 1):
            if floor <= active_floors:
                if is_full:
                    status = "🟢 Fully Active"
                    lighting = "80% Smart"
                    ventilation = "85%"
                    saving = "20%"
                else:
                    status = "🟡 Partially Active"
                    lighting = "70%"
                    ventilation = "70%"
                    saving = "30%"
            else:
                status = "🔴 Idle/Empty"
                lighting = "15% Emergency"
                ventilation = "25%"
                saving = "75%"

            floor_rows.append({
                'Floor': f'Floor {floor}',
                'Status': status,
                'Smart Lighting': lighting,
                'Ventilation': ventilation,
                'Energy Saving': saving
            })

        floor_df = pd.DataFrame(floor_rows)
        st.dataframe(
            floor_df,
            use_container_width=True
        )

        if is_full:
            st.markdown("""
                <div style='
                    background-color: #EBF5FB;
                    padding: 12px;
                    border-radius: 8px;
                '>
                    <p style='color:#1A1A1A;
                    margin:4px 0;'>
                        ✅ Motion sensor lighting
                        in corridors — lights off
                        when no movement detected
                    </p>
                    <p style='color:#1A1A1A;
                    margin:4px 0;'>
                        ✅ LED dimming during
                        late night hours
                        automatically
                    </p>
                    <p style='color:#1A1A1A;
                    margin:4px 0;'>
                        ✅ Elevator optimised
                        to reduce idle energy
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style='
                    background-color: #EBF5FB;
                    padding: 12px;
                    border-radius: 8px;
                '>
                    <p style='color:#1A1A1A;
                    margin:4px 0;'>
                        ✅ Floors {active_floors+1}
                        to {total_floors} set to
                        emergency lighting only
                    </p>
                    <p style='color:#1A1A1A;
                    margin:4px 0;'>
                        ✅ Ventilation reduced
                        to 25% on idle floors
                    </p>
                    <p style='color:#1A1A1A;
                    margin:4px 0;'>
                        ✅ Elevators restricted
                        to floors 1 to
                        {active_floors} only
                    </p>
                </div>
            """, unsafe_allow_html=True)

    with fl2:
        floor_chart = px.bar(
            floor_df,
            x='Floor',
            y='Energy Saving',
            title='Energy Saving % Per Floor',
            color='Status',
            color_discrete_map={
                '🟢 Fully Active': '#2ECC71',
                '🟡 Partially Active': '#F39C12',
                '🔴 Idle/Empty': '#E74C3C'
            }
        )
        floor_chart.update_layout(height=350)
        st.plotly_chart(
            floor_chart,
            use_container_width=True
        )

    st.divider()

    # ── TECHNIQUE 3: OCCUPANCY PATTERNS ──
    st.markdown("""
        <div style='
            background-color: #FDEBD0;
            padding: 18px;
            border-radius: 10px;
            border-left: 6px solid #D68910;
            margin-bottom: 10px;
        '>
            <h3 style='color: #1A1A1A;'>
                3️⃣ Occupancy Pattern Prediction
            </h3>
        </div>
    """, unsafe_allow_html=True)

    hours = [
        "12AM", "2AM", "4AM", "6AM",
        "8AM", "10AM", "12PM", "2PM",
        "4PM", "6PM", "8PM", "10PM"
    ]

    if is_full:
        # Full hotel - guests still leave rooms
        actual_usage = [
            88, 92, 95, 85,
            60, 45, 40, 50,
            65, 80, 90, 91
        ]
        ai_energy = [
            75, 78, 80, 72,
            52, 40, 36, 45,
            58, 72, 82, 82
        ]
        normal_energy = [
            95, 95, 95, 95,
            95, 95, 95, 95,
            95, 95, 95, 95
        ]
    else:
        base = predicted_occupancy
        actual_usage = [
            min(100, base + x)
            for x in [
                5, 8, 10, 5, -10,
                -15, -20, -15, -5,
                5, 10, 8
            ]
        ]
        ai_energy = [
            round(u * 0.85, 1)
            for u in actual_usage
        ]
        normal_energy = [100] * 12

    pattern_df = pd.DataFrame({
        'Time': hours,
        'Actual Room Usage %': actual_usage,
        'AI Optimised Energy %': ai_energy,
        'Without AI Energy %': normal_energy
    })

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=pattern_df['Time'],
        y=pattern_df['Without AI Energy %'],
        name='Without AI (Fixed Power)',
        line=dict(
            color='#E74C3C',
            width=2,
            dash='dash'
        ),
        fill=None
    ))
    fig3.add_trace(go.Scatter(
        x=pattern_df['Time'],
        y=pattern_df['AI Optimised Energy %'],
        name='With AI (Smart Power)',
        line=dict(color='#2ECC71', width=3),
        fill='tonexty',
        fillcolor='rgba(46,204,113,0.15)'
    ))
    fig3.add_trace(go.Bar(
        x=pattern_df['Time'],
        y=pattern_df['Actual Room Usage %'],
        name='Actual Room Usage %',
        marker_color='#3498DB',
        opacity=0.4
    ))
    fig3.update_layout(
        title=(
            '24-Hour Energy Pattern: '
            'AI vs Traditional System'
        ),
        height=420,
        yaxis_title='Energy / Usage %',
        legend=dict(
            orientation='h',
            y=-0.2
        )
    )
    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    if is_full:
        st.info("""
            **🤖 ML Insight for Full Hotel:**
            Even at 100% occupancy guests
            leave their rooms during the day.
            The AI detects this through
            door sensors and keycard data
            and reduces energy automatically
            — saving up to 15% even when
            fully booked!
        """)
    else:
        st.info(f"""
            **🤖 ML Insight:**
            The green shaded area shows
            energy saved by the AI system
            compared to running at fixed
            full power. With {predicted_occupancy}%
            occupancy the AI saves energy
            dynamically throughout the day.
        """)

    st.divider()

    # ── TECHNIQUE 4: SMART EQUIPMENT ──
    st.markdown("""
        <div style='
            background-color: #E8DAEF;
            padding: 18px;
            border-radius: 10px;
            border-left: 6px solid #7D3C98;
            margin-bottom: 10px;
        '>
            <h3 style='color: #1A1A1A;'>
                4️⃣ Smart Equipment Scheduling
            </h3>
        </div>
    """, unsafe_allow_html=True)

    eq1, eq2 = st.columns(2)

    with eq1:
        if is_full:
            laundry_load = "High"
            kitchen_load = "High"
            water_load = "High"
        else:
            laundry_load = "Medium"
            kitchen_load = "Medium"
            water_load = "Medium"

        equip_df = pd.DataFrame({
            'Equipment': [
                'Laundry Services',
                'Kitchen Equipment',
                'Water Heating',
                'Swimming Pool',
                'Gym Equipment'
            ],
            'Current Load': [
                laundry_load,
                kitchen_load,
                water_load,
                'Low',
                'Low'
            ],
            'AI Scheduled Time': [
                '2AM-5AM (Off-peak)',
                '6-9AM & 5-8PM',
                '5AM-7AM (Pre-peak)',
                '7AM-9PM only',
                '6AM-10PM only'
            ],
            'Energy Saving': [
                '25%', '20%',
                '30%', '15%', '10%'
            ]
        })
        st.dataframe(
            equip_df,
            use_container_width=True
        )

        st.markdown("""
            <div style='
                background-color: #F5EEF8;
                padding: 12px;
                border-radius: 8px;
                margin-top: 10px;
            '>
                <p style='color:#1A1A1A;
                margin:4px 0;'>
                    ✅ Even at full occupancy
                    laundry runs at 2AM when
                    electricity is cheapest
                </p>
                <p style='color:#1A1A1A;
                margin:4px 0;'>
                    ✅ Kitchen equipment off
                    between meal services
                </p>
                <p style='color:#1A1A1A;
                margin:4px 0;'>
                    ✅ Water heated before
                    peak demand not during it
                </p>
            </div>
        """, unsafe_allow_html=True)

    with eq2:
        equip_chart = px.bar(
            equip_df,
            x='Equipment',
            y='Energy Saving',
            title='Equipment Saving Potential',
            color='Equipment',
            color_discrete_sequence=[
                '#7D3C98', '#9B59B6',
                '#A569BD', '#C39BD3',
                '#D7BDE2'
            ],
            text='Energy Saving'
        )
        equip_chart.update_traces(
            textposition='outside'
        )
        equip_chart.update_layout(height=350)
        st.plotly_chart(
            equip_chart,
            use_container_width=True
        )

    st.divider()

    # ── TECHNIQUE 5: MAINTENANCE ──
    st.markdown("""
        <div style='
            background-color: #FADBD8;
            padding: 18px;
            border-radius: 10px;
            border-left: 6px solid #C0392B;
            margin-bottom: 10px;
        '>
            <h3 style='color: #1A1A1A;'>
                5️⃣ Predictive Maintenance Alerts
            </h3>
        </div>
    """, unsafe_allow_html=True)

    mn1, mn2 = st.columns(2)

    with mn1:
        maint_df = pd.DataFrame({
            'Equipment': [
                'AC Unit Floor 3',
                'Refrigerator Kitchen',
                'Water Heater Block B',
                'Elevator Motor',
                'Lobby Lighting'
            ],
            'Status': [
                '🔴 Abnormal',
                '🟡 Monitor',
                '🟢 Normal',
                '🟢 Normal',
                '🟡 Inefficient'
            ],
            'Extra Waste/Day': [
                '35 KWh',
                '12 KWh',
                '0 KWh',
                '0 KWh',
                '8 KWh'
            ],
            'Action': [
                '🔧 Urgent Fix',
                '🔍 Inspect',
                '✅ None',
                '✅ None',
                '🔍 Check'
            ]
        })
        st.dataframe(
            maint_df,
            use_container_width=True
        )

    with mn2:
        st.error("""
            **🔴 CRITICAL ALERT**

            AC Unit on Floor 3 is consuming
            35 KWh EXTRA per day due to
            possible malfunction.

            Monthly waste: **1,050 KWh**
            Monthly cost waste: **$126.00**

            **Action: Schedule immediate
            maintenance inspection.**
        """)
        st.warning("""
            **🟡 NOTE:**
            This waste happens even when
            the hotel is FULLY BOOKED.
            Predictive maintenance saves
            energy regardless of occupancy!
        """)

    st.divider()

    # ── FINAL SUMMARY ──
    st.subheader(
        "🏆 Complete AI Energy Action Summary"
    )

    # Calculate all savings
    if is_full:
        hvac_s = round(
            occupied_rooms * 50 * 0.15, 1
        )
        lighting_s = round(
            total_rooms * 50 * 0.08, 1
        )
        equipment_s = round(
            total_rooms * 50 * 0.07, 1
        )
        maintenance_s = round(
            total_rooms * 50 * 0.05, 1
        )
    else:
        hvac_s = round(
            empty_rooms * 50 * 0.35 +
            occupied_rooms * 50 * 0.10, 1
        )
        lighting_s = round(
            empty_rooms * 50 * 0.20, 1
        )
        equipment_s = round(
            total_rooms * 50 * 0.07, 1
        )
        maintenance_s = round(
            total_rooms * 50 * 0.05, 1
        )

    total_s = round(
        hvac_s + lighting_s +
        equipment_s + maintenance_s, 1
    )
    money_s = round(total_s * 0.12, 2)
    co2_s = round(total_s * 0.233, 2)

    summary_df = pd.DataFrame({
        'Technique': [
            'Smart HVAC',
            'Floor Lighting',
            'Equipment Scheduling',
            'Predictive Maintenance'
        ],
        'Energy Saved KWh': [
            hvac_s, lighting_s,
            equipment_s, maintenance_s
        ],
        'Money Saved $': [
            round(hvac_s * 0.12, 2),
            round(lighting_s * 0.12, 2),
            round(equipment_s * 0.12, 2),
            round(maintenance_s * 0.12, 2)
        ]
    })

    s1, s2 = st.columns(2)

    with s1:
        fig4 = px.bar(
            summary_df,
            x='Technique',
            y='Energy Saved KWh',
            title='Saving by Technique (KWh)',
            color='Technique',
            color_discrete_sequence=[
                '#2980B9', '#1E8449',
                '#7D3C98', '#C0392B'
            ],
            text='Energy Saved KWh'
        )
        fig4.update_traces(
            texttemplate='%{text} KWh',
            textposition='outside'
        )
        fig4.update_layout(height=380)
        st.plotly_chart(
            fig4,
            use_container_width=True
        )

    with s2:
        fig5 = px.pie(
            summary_df,
            values='Energy Saved KWh',
            names='Technique',
            title='Energy Saving Distribution',
            color_discrete_sequence=[
                '#2980B9', '#1E8449',
                '#7D3C98', '#C0392B'
            ]
        )
        fig5.update_layout(height=380)
        st.plotly_chart(
            fig5,
            use_container_width=True
        )

    # Metrics
    fm1, fm2, fm3, fm4 = st.columns(4)
    with fm1:
        st.metric(
            "⚡ Total Energy Saved",
            f"{total_s} KWh"
        )
    with fm2:
        st.metric(
            "💰 Money Saved",
            f"${money_s}"
        )
    with fm3:
        st.metric(
            "🌱 CO2 Reduced",
            f"{co2_s} Kg"
        )
    with fm4:
        st.metric(
            "📊 Occupancy",
            f"{predicted_occupancy}%"
        )

    # Final AI Box
    st.markdown(f"""
        <div style='
            background-color: #1F3864;
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            margin-top: 15px;
        '>
            <h2 style='color: white;'>
                🤖 AI Energy Decision Summary
            </h2>
            <p style='color: #BDE3FF;
            font-size: 16px; margin: 8px 0;'>
                Scenario: <b style='color:white;'>
                {scenario}</b>
            </p>
            <p style='color: #BDE3FF;
            font-size: 15px; margin: 8px 0;'>
                {occupied_rooms} rooms occupied
                | {empty_rooms} rooms empty
            </p>
            <p style='color: #90CAF9;
            font-size: 15px; margin: 8px 0;'>
                ⚡ {total_s} KWh saved |
                💰 ${money_s} saved |
                🌱 {co2_s} Kg CO2 reduced
            </p>
            <p style='
                color: #D5F5E3;
                font-size: 14px;
                margin-top: 15px;
                line-height: 1.8;
            '>
                This system saves energy at
                <b style='color:white;'>
                ANY occupancy level</b>
                — whether the hotel is empty
                OR fully booked — through Smart
                HVAC, Floor Management, Occupancy
                Patterns, Equipment Scheduling,
                and Predictive Maintenance.
            </p>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# Footer
st.markdown("""
    <div style='
        text-align: center;
        color: #444444;
    '>
        <p>Hotel Energy Optimizer |
        AI Energy Decision Support System</p>
    </div>
""", unsafe_allow_html=True)