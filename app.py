import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Energy Consumption Calculator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #333;
        margin-bottom: 1rem;
    }
    .energy-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .stSelectbox > div > div {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="main-header">⚡ Energy Consumption Calculator</h1>', unsafe_allow_html=True)

# Create sidebar for inputs
with st.sidebar:
    st.markdown('<h2 class="sub-header">📝 Personal Information</h2>', unsafe_allow_html=True)
    
    # Personal Information
    name = st.text_input("Enter your name:", placeholder="John Doe")
    age = st.number_input("Enter your age:", min_value=1, max_value=120, value=25)
    city = st.text_input("Enter your city:", placeholder="Mumbai")
    area = st.text_input("Enter your area name:", placeholder="Andheri")
    
    st.markdown('<h2 class="sub-header">🏠 Housing Information</h2>', unsafe_allow_html=True)
    
    # Housing Information
    flat_tenament = st.selectbox(
        "Are you living in Flat or Tenement?",
        ["Flat", "Tenement"],
        index=0
    )
    
    facility = st.selectbox(
        "What type of accommodation?",
        ["1BHK", "2BHK", "3BHK"],
        index=1
    )
    
    st.markdown('<h2 class="sub-header">🔌 Appliances</h2>', unsafe_allow_html=True)
    
    # Appliances
    ac = st.radio("Are you using AC?", ["Yes", "No"], index=1)
    fridge = st.radio("Are you using Fridge?", ["Yes", "No"], index=0)
    washing_machine = st.radio("Are you using Washing Machine?", ["Yes", "No"], index=0)

# Calculate energy consumption
def calculate_energy(facility, ac, fridge, washing_machine):
    cal_energy = 0
    
    # Base energy consumption based on facility type
    if facility == "1BHK":
        cal_energy += 2 * 0.4 + 2 * 0.8  # 2.4 kWh
    elif facility == "2BHK":
        cal_energy += 3 * 0.4 + 3 * 0.8  # 3.6 kWh
    elif facility == "3BHK":
        cal_energy += 4 * 0.4 + 4 * 0.8  # 4.8 kWh
    
    # Additional appliances
    if ac == "Yes":
        cal_energy += 3
    if fridge == "Yes":
        cal_energy += 3
    if washing_machine == "Yes":
        cal_energy += 3
    
    return cal_energy

# Main content area
if name:  # Only show results if name is entered
    # Calculate energy
    total_energy = calculate_energy(facility, ac, fridge, washing_machine)
    
    # Create columns for layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="energy-card">', unsafe_allow_html=True)
        st.markdown(f"<h2>Hello, {name}! 👋</h2>", unsafe_allow_html=True)
        st.markdown(f"<h3>Your Daily Energy Consumption</h3>", unsafe_allow_html=True)
        st.markdown(f"<h1>{total_energy:.1f} kWh</h1>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display user information
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f"**📍 Location:** {area}, {city}")
        st.markdown(f"**🏠 Housing:** {facility} {flat_tenament}")
        st.markdown(f"**👤 Age:** {age} years")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Create energy breakdown chart
        energy_breakdown = {
            'Category': ['Base Consumption', 'Air Conditioner', 'Refrigerator', 'Washing Machine'],
            'Energy (kWh)': [
                2.4 if facility == "1BHK" else 3.6 if facility == "2BHK" else 4.8,
                3 if ac == "Yes" else 0,
                3 if fridge == "Yes" else 0,
                3 if washing_machine == "Yes" else 0
            ]
        }
        
        # Filter out zero values
        df = pd.DataFrame(energy_breakdown)
        df = df[df['Energy (kWh)'] > 0]
        
        # Create pie chart
        fig_pie = px.pie(df, values='Energy (kWh)', names='Category', 
                        title='Energy Consumption Breakdown',
                        color_discrete_sequence=px.colors.qualitative.Set3)
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Energy consumption over time simulation
    st.markdown('<h2 class="sub-header">📊 Monthly Energy Projection</h2>', unsafe_allow_html=True)
    
    # Create monthly projection
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Simulate seasonal variations (higher in summer months)
    seasonal_multiplier = [0.9, 0.9, 1.0, 1.2, 1.4, 1.5, 1.5, 1.4, 1.2, 1.0, 0.9, 0.9]
    monthly_consumption = [total_energy * 30 * mult for mult in seasonal_multiplier]
    
    # Create line chart
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=months,
        y=monthly_consumption,
        mode='lines+markers',
        name='Monthly Consumption',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8)
    ))
    
    fig_line.update_layout(
        title='Projected Monthly Energy Consumption',
        xaxis_title='Month',
        yaxis_title='Energy Consumption (kWh)',
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig_line, use_container_width=True)
    
    # Energy saving tips
    st.markdown('<h2 class="sub-header">💡 Energy Saving Tips</h2>', unsafe_allow_html=True)
    
    col3, col4, col5 = st.columns(3)
    
    with col3:
        st.markdown("""
        **🌡️ Air Conditioning**
        - Set temperature to 24-26°C
        - Use fans to circulate air
        - Keep doors and windows closed
        - Regular maintenance
        """)
    
    with col4:
        st.markdown("""
        **❄️ Refrigerator**
        - Set optimal temperature (37-40°F)
        - Don't overfill
        - Check door seals
        - Defrost regularly
        """)
    
    with col5:
        st.markdown("""
        **🔌 General Tips**
        - Use LED bulbs
        - Unplug unused devices
        - Use power strips
        - Regular appliance maintenance
        """)
    
    # Cost calculation
    st.markdown('<h2 class="sub-header">💰 Cost Estimation</h2>', unsafe_allow_html=True)
    
    # Assuming average electricity rate in India
    rate_per_kwh = st.slider("Electricity Rate (₹/kWh)", 2.0, 10.0, 5.0, 0.1)
    
    daily_cost = total_energy * rate_per_kwh
    monthly_cost = daily_cost * 30
    yearly_cost = monthly_cost * 12
    
    cost_col1, cost_col2, cost_col3 = st.columns(3)
    
    with cost_col1:
        st.metric("Daily Cost", f"₹{daily_cost:.2f}")
    
    with cost_col2:
        st.metric("Monthly Cost", f"₹{monthly_cost:.2f}")
    
    with cost_col3:
        st.metric("Yearly Cost", f"₹{yearly_cost:.2f}")

else:
    st.info("👈 Please enter your name in the sidebar to get started!")
    
    # Show sample visualization
    st.markdown('<h2 class="sub-header">📊 Sample Energy Breakdown</h2>', unsafe_allow_html=True)
    
    sample_data = {
        'Appliance': ['Base Consumption', 'Air Conditioner', 'Refrigerator', 'Washing Machine'],
        'Energy (kWh)': [3.6, 3.0, 3.0, 3.0]
    }
    
    df_sample = pd.DataFrame(sample_data)
    fig_sample = px.bar(df_sample, x='Appliance', y='Energy (kWh)', 
                       title='Sample Energy Consumption by Appliance',
                       color='Energy (kWh)',
                       color_continuous_scale='Blues')
    fig_sample.update_layout(height=400)
    st.plotly_chart(fig_sample, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit and Plotly | Energy Consumption Calculator")
st.markdown(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")