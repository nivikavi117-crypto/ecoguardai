from streamlit_js_eval import get_geolocation
import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation
import plotly.graph_objects as go
from PIL import Image, ImageDraw, ImageFont
import random
import datetime

# --- CONFIGURATION & STYLING ---
st.set_page_config(page_title="EcoGuard AI", page_icon="🌲", layout="wide")

# Modern Forest Dark Mode Theme CSS
st.markdown("""
    <style>
    .main { background-color: #0b130a; color: #e1e7e0; }
    .stApp { background-color: #0b130a; }
    h1, h2, h3 { color: #4caf50 !important; font-family: 'Segoe UI', sans-serif; }
    .reportview-container .main .block-container{ max-width: 1200px; }
    div.stButton > button:first-child {
        background-color: #2e7d32; color: white; border-radius: 8px;
        border: none; padding: 10px 24px; font-weight: bold;
    }
    div.stButton > button:first-child:hover { background-color: #1b5e20; }
    .metric-card {
        background-color: #142213; padding: 15px; border-radius: 10px;
        border: 1px solid #2e7d32; margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CORE BACKEND ENGINES ---

# 1. Fire Risk Prediction Engine
def predict_fire_risk(temp, humidity, wind_speed):
    # Logical environmental formula: Higher temp, lower humidity, higher wind = higher risk
    risk = (temp * 1.5) - (humidity * 0.5) + (wind_speed * 0.8)
    risk = max(0, min(100, risk))  # Clamp between 0 and 100
    return round(risk, 2)

# 2. Mock AI Object Detection Engine (YOLO Simulation)
def run_mock_yolo(animal_type):
    # Generates dynamic coordinates and dimensions for bounding box
    img = Image.new('RGB', (500, 350), color=(30, 45, 30))
    draw = ImageDraw.Draw(img)
    
    # Draw simple representative graphics since it's a simulated feed
    if animal_type == "Elephant":
        draw.ellipse([150, 100, 350, 260], fill=(100, 100, 100)) # Body
        draw.rectangle([120, 140, 170, 240], fill=(90, 90, 90))  # Trunk
        label = "Elephant Detected"
        confidence = random.randint(91, 98)
        distance = random.randint(150, 450) # Meters from boundary
    elif animal_type == "Tiger":
        draw.rectangle([160, 120, 340, 240], fill=(230, 120, 20)) # Body
        draw.ellipse([300, 100, 360, 160], fill=(200, 100, 10))   # Head
        label = "Tiger Detected"
        confidence = random.randint(88, 96)
        distance = random.randint(300, 600)
    else:
        draw.text((180, 160), "Clear Forest Boundary", fill=(100, 200, 100))
        label = "No Threat"
        confidence = 0
        distance = 1500
        
    if animal_type != "No Animal":
        # Draw simulated bounding box bounding
        draw.rectangle([100, 80, 400, 280], outline=(255, 50, 50), width=4)
        draw.rectangle([100, 50, 280, 80], fill=(255, 50, 50))
        draw.text((110, 55), f"{label}: {confidence}%", fill=(255, 255, 255))
        
    return img, label, confidence, distance

# 3. Emergency Alert Script Wrapper (Twilio Simulation)
def send_emergency_sms(alert_type, details, location="Grid 4B [11.0181, 76.9737]"):
    sms_body = f"⚠️ ECOGUARD ALERT: {alert_type} confirmed at {location}. Info: {details}. Evacuation routes updated."
    
    # Python Twilio code implementation framework
    # In a real environment, you would uncomment the lines below:
    # from twilio.rest import Client
    # account_sid = 'YOUR_ACCOUNT_SID'
    # auth_token = 'YOUR_AUTH_TOKEN'
    # client = Client(account_sid, auth_token)
    # message = client.messages.create(body=sms_body, from_='+1234567890', to='+919876543210')
    
    # Return beautiful execution trace for presentation logs
    return True, sms_body

# --- APP LAYOUT & PRESENTATION LAYER ---

st.title("🌲 EcoGuard AI: Forest Safety & Disaster Prediction")
st.markdown("---")

# Sidebar Application Selector Mode Switch
view_mode = st.sidebar.radio("Select Interface View:", ["🏠 Citizen Mobile App App", "🛡️ Department Admin Dashboard"])

# Simulated Environment Coordinates (Western Ghats, India Base Location)
base_lat, base_lon = 11.0181, 76.9737
village_coords = [11.0250, 76.9850]
danger_coords = [11.0150, 76.9700]

# Global State Variables Simulation via sliders
st.sidebar.markdown("### Live Telemetry Control")
input_temp = st.sidebar.slider("Temperature (°C)", 15, 50, 42)
input_hum = st.sidebar.slider("Humidity (%)", 5, 95, 12)
input_wind = st.sidebar.slider("Wind Speed (km/h)", 0, 60, 35)
        import requests
        try:
            geo_data = requests.get('https://ipapi.co', timeout=3).json()
            base_lat, base_lon = geo_data.get('latitude', 11.0181), geo_data.get('longitude', 76.9737)
        except:
            base_lat, base_lon = 11.0181, 76.9737

base_lat, base_lon = (loc['coords']['latitude'], loc['coords']['longitude']) if loc else (11.0181, 76.9737)

fire_risk_score = predict_fire_risk(input_temp, input_hum, input_wind)
img_feed, ai_label, ai_conf, animal_dist = run_mock_yolo(selected_feed)

# Determine Threat States
fire_alert = fire_risk_score > 70
animal_alert = selected_feed != "No Animal" and animal_dist < 500
system_trigger = fire_alert or animal_alert

# Build Folium Mapping Solution
m = folium.Map(location=[base_lat, base_lon], zoom_start=14, tiles="CartoDB dark_matter")

# Add Static Village Point
folium.Marker(location=village_coords, popup="Annamalai Village Grid", icon=folium.Icon(color='green', icon='home')).add_to(m)
# --- Extra Safest Route 1 (Teal Color) ---
alt_safe_path_1 = [[11.0180, 76.9700], [11.0250, 76.9780], [11.0250, 76.9850]]
folium.PolyLine(alt_safe_path_1, color="#00ffcc", weight=5, opacity=0.8, tooltip="Alternative Safe Route 1").add_to(m)

# --- Extra Safest Route 2 (Light Green Color) ---
alt_safe_path_2 = [[11.0180, 76.9700], [11.0150, 76.9750], [11.0250, 76.9850]]
folium.PolyLine(alt_safe_path_2, color="#76ff03", weight=5, opacity=0.8, tooltip="Alternative Safe Route 2").add_to(m)

# Dynamic Fire Heat/Danger Radius Generation
if fire_risk_score > 50:
    folium.Circle(location=danger_coords, radius=600, color='red', fill=True, fill_color='red', fill_opacity=0.4, popup=f"Fire Hazard Matrix Risk: {fire_risk_score}%").add_to(m)

# Dynamic Wild Animal Threat Position Generation
if selected_feed != "No Animal":
  folium.Marker(location=[11.0190, 76.9780], popup=f"ALERT: {ai_label}", icon=folium.Icon(color='orange', icon='warning')).add_to(m)

# Dynamic Routing Logic Engine Matrix Lines
standard_route = [[11.0120, 76.9650], danger_coords, village_coords]
safe_alternative_route = [[11.0120, 76.9650], [11.0300, 76.9700], [11.0320, 76.9820], village_coords]

if system_trigger:
    # Danger Detected: Draw standard path in Red (Blocked) and Evacuation in Green
    folium.PolyLine(standard_route, color="red", weight=4, opacity=0.5, tooltip="BLOCKED PATH - HIGH RISK").add_to(m)
    folium.PolyLine(safe_alternative_route, color="green", weight=6, opacity=0.9, tooltip="RECOMMENDED SAFE ROUTE").add_to(m)
else:
    # All Clear: Draw standard path in Blue
    folium.PolyLine(standard_route, color="blue", weight=5, opacity=0.8, tooltip="Standard Fast Route Clear").add_to(m)


# Render Selected Interface View Layout
if view_mode == "🏠 Citizen Mobile App App":
    st.subheader("📱 Mobile Companion App Layer (Citizen Safety UI)")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Real-Time Safe Navigation Map")
        st_folium(m, width=700, height=450)
        
    with col2:
        st.markdown("### Local Status Alerts")
        if system_trigger:
            st.error("🚨 EMERGENCY EVACUATION ACTIVE")
            if fire_alert:
                st.markdown(f"<div class='metric-card'>🔥 <b>Forest Fire Threat High:</b> Risk score calculated at {fire_risk_score}% due to extreme dry weather conditions.</div>", unsafe_allow_html=True)
            if animal_alert:
                st.markdown(f"<div class='metric-card'>🐘 <b>Wildlife Boundary Intrusion:</b> {ai_label} detected at {animal_dist}m from perimeter fence lines!</div>", unsafe_allow_html=True)
            st.success("🛣️ Dynamic Bypass Active: Follow the **Green Navigation Path** on your screen.")
        else:
            st.success("✅ ALL CLEAR - ENVIRONMENT STABLE")
            st.info("ℹ️ Forest paths are currently evaluated as safe. Normal movement permitted.")

else:
    st.subheader("🛡️ Administrative Dashboard (Forest & Emergency Services Core)")
    
    # Header Metrics Matrix
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="Calculated Fire Probability Index", value=f"{fire_risk_score}%", delta="HIGH RISK" if fire_alert else "NORMAL", delta_color="inverse")
    with m2:
        st.metric(label="CCTV Neural Vision State", value=ai_label if selected_feed != "No Animal" else "No Threat Detected")
    with m3:
        st.metric(label="Threat Gateway Trigger Link", value="EMERGENCY ALERT" if system_trigger else "SECURE")
        
    st.markdown("---")
    
    col_left, col_right = st.columns(2)

    
    with col_left:
        st.markdown("### CCTV Infrastructure Neural Feed Scan")
        st.image(img_feed, use_container_width=True)
        
    with col_right:
        st.markdown("### Telemetry Operations & Early Dispatch Logs")
        
        # Test Live Dispatch Alert System Feature
        if st.button("Simulate Early Automated Dispatch Alert Line"):
            success, log_body = send_emergency_sms(
                "CRITICAL THREAT BROADCAST", 
                f"Fire index at {fire_risk_score}%, Vision system reports {ai_label} at {animal_dist}m"
            )
            if success:
                st.info("📨 **Twilio Core API Stack Call Sim:** Communication package compiled and dispatched successfully!")
                st.code(log_body, language="text")
                
        st.markdown("#### System Operations Log Matrix")
        st.text_area(label="Live Audit Feed", value=f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Core Model Scan Complete. Environment Stable.\n" +
                     (f"[{datetime.datetime.now().strftime('%H:%M:%S')}] WARNING: Fire threat model flag raised.\n" if fire_alert else "") +
                     (f"[{datetime.datetime.now().strftime('%H:%M:%S')}] WARNING: AI Boundary Alert: Intrusion detected.\n" if selected_feed != "No Animal" else ""),
                     height=150)
