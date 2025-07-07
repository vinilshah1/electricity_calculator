import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Energy Consumption Calculator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

    # Custom CSS for darker muted theme
st.markdown("""
<style>
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1c2128, #161b22);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
        border: 1px solid #30363d;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #161b22, #1c2128);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #30363d;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    }
    
    .energy-result {
        background: linear-gradient(135deg, #21262d, #161b22);
        color: #7c8896;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        border: 1px solid #3d444d;
    }
    
    .stSelectbox > div > div {
        background-color: #21262d;
        color: #c9d1d9;
        border: 1px solid #30363d;
    }
    
    .stTextInput > div > div > input {
        background-color: #21262d;
        color: #c9d1d9;
        border: 1px solid #30363d;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #3d444d, #21262d);
        color: #c9d1d9;
        border: 1px solid #30363d;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #484f58, #3d444d);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    }
    
    .sidebar .stSelectbox > div > div {
        background-color: #21262d;
        color: #c9d1d9;
    }
    
    .device-section {
        background: linear-gradient(135deg, #161b22, #1c2128);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 3px solid #484f58;
        border: 1px solid #30363d;
    }
    
    h1, h2, h3 {
        color: #7c8896;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background-color: #21262d;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #161b22;
        color: #c9d1d9;
        border-radius: 8px;
        margin: 0.2rem;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #1c2128;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #3d444d !important;
        color: #c9d1d9 !important;
    }
    
    .stRadio > div {
        background-color: #161b22;
        padding: 0.5rem;
        border-radius: 8px;
        border: 1px solid #30363d;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'calculated' not in st.session_state:
    st.session_state.calculated = False
if 'energy_data' not in st.session_state:
    st.session_state.energy_data = {}

# Header
st.markdown("""
<div class="main-header">
    <h1>⚡ Energy Consumption Calculator</h1>
    <p style="font-size: 1.2rem; color: #8be9fd;">Calculate your home's energy usage and carbon footprint</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for user information
st.sidebar.header("🏠 Personal Information")
name = st.sidebar.text_input("Enter your name:", placeholder="Your name")
age = st.sidebar.number_input("Enter your age:", min_value=1, max_value=120, value=25)
city = st.sidebar.text_input("Enter your city:", placeholder="Your city")
area = st.sidebar.text_input("Enter your area name:", placeholder="Your area")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("## 🏡 Home Configuration")
    
    # Home type selection
    flat_tenement = st.selectbox(
        "Are you living in Flat or Tenement?",
        ["Flat", "Tenement"],
        index=0
    )
    
    # BHK selection
    facility = st.selectbox(
        "Select your home type:",
        ["1BHK", "2BHK", "3BHK"],
        index=0
    ).lower()
    
    st.markdown("## 📱 Appliances & Devices")
    
    st.markdown('<div class="device-section">', unsafe_allow_html=True)
    
    # AC selection
    ac = st.radio("Are you using AC?", ["Yes", "No"], index=1).lower()
    if ac == "yes":
        num_ac = st.number_input("Number of ACs:", min_value=1, max_value=10, value=1)
    else:
        num_ac = 0
    
    # Fridge selection  
    fridge = st.radio("Are you using Fridge?", ["Yes", "No"], index=1).lower()
    
    # Washing Machine selection (fixing the typo from original code)
    wm = st.radio("Are you using Washing Machine?", ["Yes", "No"], index=1).lower()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Weekly Usage Pattern
    st.markdown("## 📅 Weekly Usage Pattern")
    st.markdown('<div class="device-section">', unsafe_allow_html=True)
    
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekly_usage = {}
    
    st.markdown("### Enter hours of usage for each day:")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        for i, day in enumerate(days[:4]):
            if ac == "yes":
                weekly_usage[f"{day}_ac"] = st.number_input(f"AC hours on {day}:", min_value=0, max_value=24, value=0, key=f"ac_{day}")
            else:
                weekly_usage[f"{day}_ac"] = 0
                
            if fridge == "yes":
                weekly_usage[f"{day}_fridge"] = st.number_input(f"Fridge hours on {day}:", min_value=0, max_value=24, value=24, key=f"fridge_{day}")
            else:
                weekly_usage[f"{day}_fridge"] = 0
                
            if wm == "yes":
                weekly_usage[f"{day}_wm"] = st.number_input(f"Washing Machine hours on {day}:", min_value=0, max_value=24, value=0, key=f"wm_{day}")
            else:
                weekly_usage[f"{day}_wm"] = 0
            
            st.markdown("---")
    
    with col_right:
        for i, day in enumerate(days[4:]):
            if ac == "yes":
                weekly_usage[f"{day}_ac"] = st.number_input(f"AC hours on {day}:", min_value=0, max_value=24, value=0, key=f"ac_{day}")
            else:
                weekly_usage[f"{day}_ac"] = 0
                
            if fridge == "yes":
                weekly_usage[f"{day}_fridge"] = st.number_input(f"Fridge hours on {day}:", min_value=0, max_value=24, value=24, key=f"fridge_{day}")
            else:
                weekly_usage[f"{day}_fridge"] = 0
                
            if wm == "yes":
                weekly_usage[f"{day}_wm"] = st.number_input(f"Washing Machine hours on {day}:", min_value=0, max_value=24, value=0, key=f"wm_{day}")
            else:
                weekly_usage[f"{day}_wm"] = 0
            
            st.markdown("---")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Calculate button
if st.button("🔍 Calculate Energy Consumption", type="primary"):
    cal_energy = 0
    energy_breakdown = {}
    weekly_breakdown = {}
    
    # Base energy calculation for home type
    if facility == "1bhk":
        base_energy = 2 * 0.4 + 2 * 0.8
        energy_breakdown["Base Lighting & Outlets"] = base_energy
    elif facility == "2bhk":
        base_energy = 3 * 0.4 + 3 * 0.8
        energy_breakdown["Base Lighting & Outlets"] = base_energy
    elif facility == "3bhk":
        base_energy = 4 * 0.4 + 4 * 0.8
        energy_breakdown["Base Lighting & Outlets"] = base_energy
    else:
        st.error("Wrong input for home type")
        st.stop()
    
    # Calculate weekly energy consumption
    total_weekly_energy = 0
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    for day in days:
        day_energy = base_energy  # Base energy for each day
        
        # AC energy calculation (3 kWh per AC per hour)
        if ac == "yes":
            ac_energy = weekly_usage[f"{day}_ac"] * 3 * num_ac
            day_energy += ac_energy
        
        # Fridge energy calculation (3 kWh per hour)
        if fridge == "yes":
            fridge_energy = weekly_usage[f"{day}_fridge"] * 3
            day_energy += fridge_energy
        
        # Washing Machine energy calculation (3 kWh per hour)
        if wm == "yes":
            wm_energy = weekly_usage[f"{day}_wm"] * 3
            day_energy += wm_energy
        
        weekly_breakdown[day] = day_energy
        total_weekly_energy += day_energy
    
    # Calculate average daily energy
    cal_energy = total_weekly_energy / 7
    
    # Calculate appliance-wise breakdown for the week
    total_ac_energy = 0
    total_fridge_energy = 0
    total_wm_energy = 0
    
    if ac == "yes":
        for day in days:
            total_ac_energy += weekly_usage[f"{day}_ac"] * 3 * num_ac
        energy_breakdown["Air Conditioning"] = total_ac_energy / 7
    
    if fridge == "yes":
        for day in days:
            total_fridge_energy += weekly_usage[f"{day}_fridge"] * 3
        energy_breakdown["Refrigerator"] = total_fridge_energy / 7
    
    if wm == "yes":
        for day in days:
            total_wm_energy += weekly_usage[f"{day}_wm"] * 3
        energy_breakdown["Washing Machine"] = total_wm_energy / 7
    
    # Store results
    st.session_state.calculated = True
    st.session_state.energy_data = {
        'daily_kwh': cal_energy,
        'weekly_kwh': total_weekly_energy,
        'monthly_kwh': cal_energy * 30,
        'yearly_kwh': cal_energy * 365,
        'breakdown': energy_breakdown,
        'weekly_breakdown': weekly_breakdown,
        'carbon_footprint': cal_energy * 0.82 * 365,  # kg CO2 per year
        'estimated_cost': cal_energy * 30 * 5  # Assuming ₹5 per kWh
    }

# Display results
if st.session_state.calculated and st.session_state.energy_data:
    data = st.session_state.energy_data
    
    with col2:
        st.markdown("## 📊 Energy Summary")
        
        # Energy metrics
        st.markdown(f"""
        <div class="energy-result">
            <h3>Daily Consumption</h3>
            <h2>{data['daily_kwh']:.2f} kWh</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <h4>📅 Weekly: {data['weekly_kwh']:.2f} kWh</h4>
            <h4>📅 Monthly: {data['monthly_kwh']:.2f} kWh</h4>
            <h4>📈 Yearly: {data['yearly_kwh']:.2f} kWh</h4>
            <h4>💰 Est. Monthly Cost: ₹{data['estimated_cost']:.2f}</h4>
            <h4>🌍 Carbon Footprint: {data['carbon_footprint']:.2f} kg CO2/year</h4>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed breakdown
    st.markdown("## 📈 Energy Breakdown Analysis")
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Weekly consumption by day
        if 'weekly_breakdown' in data:
            weekly_df = pd.DataFrame(list(data['weekly_breakdown'].items()), columns=['Day', 'Energy (kWh)'])
            
            fig_weekly = px.bar(weekly_df, x='Day', y='Energy (kWh)',
                              title="Weekly Energy Consumption by Day",
                              color='Energy (kWh)',
                              color_continuous_scale='Viridis')
            
            fig_weekly.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#c9d1d9',
                xaxis=dict(tickangle=45)
            )
            
            st.plotly_chart(fig_weekly, use_container_width=True)
        
        # Pie chart for appliance breakdown
        if data['breakdown']:
            df_breakdown = pd.DataFrame(list(data['breakdown'].items()), columns=['Appliance', 'Energy (kWh)'])
            
            fig_pie = px.pie(df_breakdown, values='Energy (kWh)', names='Appliance', 
                           title="Average Daily Energy by Appliance",
                           color_discrete_sequence=px.colors.qualitative.Set3)
            
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#c9d1d9'
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
    
    with col4:
        # Bar chart for appliance breakdown
        if data['breakdown']:
            fig_bar = px.bar(df_breakdown, x='Appliance', y='Energy (kWh)',
                           title="Average Daily Energy by Appliance",
                           color='Energy (kWh)',
                           color_continuous_scale='Viridis')
            
            fig_bar.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#c9d1d9',
                xaxis=dict(tickangle=45)
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Weekly data table
        if 'weekly_breakdown' in data:
            st.markdown("### 📊 Weekly Consumption Details")
            weekly_df = pd.DataFrame(list(data['weekly_breakdown'].items()), columns=['Day', 'Energy (kWh)'])
            weekly_df['Energy (kWh)'] = weekly_df['Energy (kWh)'].round(2)
            st.dataframe(weekly_df, use_container_width=True, hide_index=True)
    
    # Recommendations
    st.markdown("## 💡 Energy Saving Recommendations")
    
    recommendations = []
    if data['daily_kwh'] > 10:
        recommendations.append("⚠️ Higher energy consumption detected. Consider energy-efficient appliances.")
    if 'Air Conditioning' in data['breakdown']:
        recommendations.append("❄️ Use AC efficiently - set temperature to 24°C when possible.")
    if 'Refrigerator' in data['breakdown']:
        recommendations.append("🧊 Keep refrigerator at optimal temperature for efficiency.")
    
    recommendations.extend([
        "🌱 Use energy-efficient appliances with high star ratings",
        "🔌 Unplug devices when not in use",
        "💡 Use LED bulbs for better energy efficiency",
        "⏰ Use appliances during off-peak hours when possible"
    ])
    
    for rec in recommendations:
        st.markdown(f"- {rec}")
    
    # Data table
    st.markdown("## 📋 Detailed Energy Data")
    
    summary_data = {
        'Metric': ['Daily Consumption (Average)', 'Weekly Consumption', 'Monthly Consumption', 'Yearly Consumption', 
                  'Monthly Cost Estimate', 'Carbon Footprint (Annual)'],
        'Value': [f"{data['daily_kwh']:.2f} kWh", f"{data['weekly_kwh']:.2f} kWh", 
                 f"{data['monthly_kwh']:.2f} kWh", f"{data['yearly_kwh']:.2f} kWh", 
                 f"₹{data['estimated_cost']:.2f}", f"{data['carbon_footprint']:.2f} kg CO2"],
        'Category': ['Energy', 'Energy', 'Energy', 'Energy', 'Cost', 'Environment']
    }
    
    df_summary = pd.DataFrame(summary_data)
    st.dataframe(df_summary, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #484f58; padding: 2rem;">
    <p>⚡ Energy Consumption Calculator | Built with Streamlit & Python</p>
    <p>🌱 Help reduce your carbon footprint by monitoring your energy usage</p>
</div>
""", unsafe_allow_html=True)