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
selected_feed = st.sidebar.selectbox("Simulate Camera Feed:", ["No Animal", "Elephant", "Tiger"])
import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="EcoGuard AI",
    page_icon="🌲",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #071007;
        color: white;
    }

    h1, h2, h3 {
        color: #4CAF50 !important;
    }

    .weather-card {
        background-color: #142213;
        border: 1px solid #2e7d32;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 12px;
    }

    .location-card {
        background-color: #101810;
        border: 1px solid #2e7d32;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 15px;
    }

    .risk-card {
        background-color: #24140d;
        border: 1px solid #ff5722;
        border-radius: 12px;
        padding: 18px;
        margin-top: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# GET CURRENT DEVICE LOCATION
# ============================================================

location = streamlit_geolocation(
    key="current_gps"
)


# ============================================================
# CHECK GPS
# ============================================================

if (
    location
    and location.get("latitude") is not None
    and location.get("longitude") is not None
):

    base_lat = float(location["latitude"])
    base_lon = float(location["longitude"])

    st.session_state["gps_data"] = {
        "lat": base_lat,
        "lon": base_lon
    }

    gps_available = True

else:

    base_lat = None
    base_lon = None

    gps_available = False


# ============================================================
# STOP IF GPS NOT AVAILABLE
# ============================================================

if not gps_available:

    st.title("🌲 EcoGuard AI")

    st.warning(
        "📍 Current location is not detected."
    )

    st.info(
        "Please allow location permission in your browser."
    )

    if st.button("🔄 Get My Current Location"):

        st.rerun()

    st.stop()


# ============================================================
# REVERSE GEOCODING
# GPS → CITY / DISTRICT / STATE
# ============================================================

@st.cache_data(ttl=300)
def get_location_name(latitude, longitude):

    try:

        url = "https://nominatim.openstreetmap.org/reverse"

        params = {
            "lat": latitude,
            "lon": longitude,
            "format": "json",
            "zoom": 10,
            "addressdetails": 1
        }

        headers = {
            "User-Agent": "EcoGuardAI/1.0"
        }

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:

            data = response.json()

            address = data.get("address", {})

            city = (
                address.get("city")
                or address.get("town")
                or address.get("municipality")
                or address.get("village")
                or address.get("county")
                or "Unknown Location"
            )

            district = (
                address.get("state_district")
                or address.get("county")
                or ""
            )

            state = (
                address.get("state")
                or ""
            )

            return city, district, state

    except Exception:
        pass

    return "Unknown Location", "", ""


city_name, district_name, state_name = get_location_name(
    base_lat,
    base_lon
)


# ============================================================
# LIVE WEATHER
# ============================================================

@st.cache_data(ttl=300)
def get_live_weather(latitude, longitude):

    try:

        weather_url = "https://api.open-meteo.com/v1/forecast"

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "wind_speed_10m"
            ),
            "timezone": "auto"
        }

        response = requests.get(
            weather_url,
            params=params,
            timeout=10
        )

        if response.status_code == 200:

            data = response.json()

            current = data.get("current", {})

            temperature = current.get(
                "temperature_2m"
            )

            humidity = current.get(
                "relative_humidity_2m"
            )

            wind_speed = current.get(
                "wind_speed_10m"
            )

            return (
                temperature,
                humidity,
                wind_speed
            )

    except Exception:
        pass

    return None, None, None


temperature, humidity, wind_speed = get_live_weather(
    base_lat,
    base_lon
)


# ============================================================
# FIRE RISK CALCULATION
# ============================================================

def calculate_fire_risk(
    temperature,
    humidity,
    wind_speed
):

    if (
        temperature is None
        or humidity is None
        or wind_speed is None
    ):
        return 0, "Unknown"

    score = 0

    # Temperature
    if temperature >= 40:
        score += 40

    elif temperature >= 35:
        score += 30

    elif temperature >= 30:
        score += 20

    elif temperature >= 25:
        score += 10


    # Humidity
    if humidity <= 20:
        score += 35

    elif humidity <= 30:
        score += 25

    elif humidity <= 40:
        score += 15

    elif humidity <= 50:
        score += 5


    # Wind
    if wind_speed >= 30:
        score += 25

    elif wind_speed >= 20:
        score += 18

    elif wind_speed >= 10:
        score += 10

    else:
        score += 5


    score = min(score, 100)


    if score >= 75:
        risk = "VERY HIGH"

    elif score >= 55:
        risk = "HIGH"

    elif score >= 35:
        risk = "MEDIUM"

    else:
        risk = "LOW"


    return score, risk


fire_score, fire_risk = calculate_fire_risk(
    temperature,
    humidity,
    wind_speed
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "## 🌲 EcoGuard AI"
    )

    st.markdown(
        "### 📍 Live Location"
    )

    st.success(
        city_name
    )

    st.write(
        f"Latitude: {base_lat:.6f}"
    )

    st.write(
        f"Longitude: {base_lon:.6f}"
    )

    st.markdown("---")

    st.markdown(
        "### 🌦️ Live Telemetry"
    )


    # Temperature
    if temperature is not None:

        st.metric(
            "🌡️ Temperature (°C)",
            f"{temperature:.1f}"
        )

    else:

        st.metric(
            "🌡️ Temperature (°C)",
            "N/A"
        )


    # Humidity
    if humidity is not None:

        st.metric(
            "💧 Humidity (%)",
            f"{humidity:.0f}"
        )

    else:

        st.metric(
            "💧 Humidity (%)",
            "N/A"
        )


    # Wind
    if wind_speed is not None:

        st.metric(
            "💨 Wind Speed (km/h)",
            f"{wind_speed:.1f}"
        )

    else:

        st.metric(
            "💨 Wind Speed (km/h)",
            "N/A"
        )


    st.markdown("---")

    if st.button(
        "🔄 Refresh Location & Weather"
    ):

        st.cache_data.clear()

        st.rerun()


# ============================================================
# MAIN TITLE
# ============================================================

st.title(
    "🌲 EcoGuard AI"
)

st.subheader(
    "📱 Citizen Safety & Forest Fire Monitoring"
)


# ============================================================
# CURRENT LOCATION CARD
# ============================================================

st.markdown(
    f"""
    <div class="location-card">

    <h3>📍 Current Location</h3>

    <b>City / Town:</b> {city_name}<br><br>

    <b>District:</b> {district_name}<br><br>

    <b>State:</b> {state_name}<br><br>

    <b>Latitude:</b> {base_lat:.6f}<br><br>

    <b>Longitude:</b> {base_lon:.6f}

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# WEATHER SECTION
# ============================================================

st.subheader(
    "🌦️ Live Local Weather"
)


weather_col1, weather_col2, weather_col3 = st.columns(3)


with weather_col1:

    st.markdown(
        '<div class="weather-card">',
        unsafe_allow_html=True
    )

    if temperature is not None:

        st.metric(
            "🌡️ Temperature",
            f"{temperature:.1f} °C"
        )

    else:

        st.metric(
            "🌡️ Temperature",
            "N/A"
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


with weather_col2:

    st.markdown(
        '<div class="weather-card">',
        unsafe_allow_html=True
    )

    if humidity is not None:

        st.metric(
            "💧 Humidity",
            f"{humidity:.0f} %"
        )

    else:

        st.metric(
            "💧 Humidity",
            "N/A"
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


with weather_col3:

    st.markdown(
        '<div class="weather-card">',
        unsafe_allow_html=True
    )

    if wind_speed is not None:

        st.metric(
            "💨 Wind Speed",
            f"{wind_speed:.1f} km/h"
        )

    else:

        st.metric(
            "💨 Wind Speed",
            "N/A"
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# FIRE RISK
# ============================================================

st.subheader(
    "🔥 Local Forest Fire Risk"
)


if fire_risk == "VERY HIGH":

    st.error(
        f"🚨 VERY HIGH FIRE RISK — {fire_score}%"
    )

elif fire_risk == "HIGH":

    st.warning(
        f"🔥 HIGH FIRE RISK — {fire_score}%"
    )

elif fire_risk == "MEDIUM":

    st.warning(
        f"⚠️ MEDIUM FIRE RISK — {fire_score}%"
    )

elif fire_risk == "LOW":

    st.success(
        f"🟢 LOW FIRE RISK — {fire_score}%"
    )

else:

    st.info(
        "Fire risk data unavailable."
    )


# ============================================================
# SAFE NAVIGATION MAP
# ============================================================

st.subheader(
    "🗺️ Real-Time Safe Navigation Map"
)


# Current location map
m = folium.Map(
    location=[
        base_lat,
        base_lon
    ],
    zoom_start=14,
    tiles="CartoDB dark_matter"
)


# ============================================================
# CURRENT LOCATION MARKER
# ============================================================

folium.Marker(
    [
        base_lat,
        base_lon
    ],
    popup=(
        f"<b>📍 You are here</b><br>"
        f"{city_name}<br>"
        f"Lat: {base_lat:.6f}<br>"
        f"Lon: {base_lon:.6f}"
    ),
    tooltip=(
        f"📍 Current Location - {city_name}"
    ),
    icon=folium.Icon(
        color="green",
        icon="home"
    )
).add_to(m)


# ============================================================
# FIRE RISK CIRCLE
# ============================================================

if fire_risk in ["HIGH", "VERY HIGH"]:

    folium.Circle(
        location=[
            base_lat,
            base_lon
        ],
        radius=1500,
        popup=(
            f"🔥 {fire_risk} Fire Risk Area"
        ),
        tooltip=(
            f"🔥 {fire_risk} Fire Risk"
        ),
        color="red",
        fill=True,
        fill_opacity=0.25
    ).add_to(m)


# ============================================================
# SAFE AREA
# ============================================================

safe_lat = base_lat + 0.005
safe_lon = base_lon + 0.005


folium.Marker(
    [
        safe_lat,
        safe_lon
    ],
    popup="🟢 Suggested Safe Area",
    tooltip="🟢 Safe Area",
    icon=folium.Icon(
        color="green",
        icon="ok"
    )
).add_to(m)


# ============================================================
# SAFE ROUTE
# ============================================================

folium.PolyLine(
    locations=[
        [
            base_lat,
            base_lon
        ],
        [
            safe_lat,
            safe_lon
        ]
    ],
    color="green",
    weight=5,
    opacity=0.8,
    tooltip="🟢 Suggested Safe Route"
).add_to(m)


# ============================================================
# SHOW MAP
# ============================================================

st_folium(
    m,
    width=1100,
    height=550
)


# ============================================================
# LOCATION + WEATHER SUMMARY
# ============================================================

st.markdown("---")

st.subheader(
    "📊 Current Area Summary"
)

summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)


with summary_col1:

    st.metric(
        "📍 Location",
        city_name
    )


with summary_col2:

    if temperature is not None:

        st.metric(
            "🌡️ Temperature",
            f"{temperature:.1f} °C"
        )

    else:

        st.metric(
            "🌡️ Temperature",
            "N/A"
        )


with summary_col3:

    if humidity is not None:

        st.metric(
            "💧 Humidity",
            f"{humidity:.0f}%"
        )

    else:

        st.metric(
            "💧 Humidity",
            "N/A"
        )


with summary_col4:

    if wind_speed is not None:

        st.metric(
            "💨 Wind",
            f"{wind_speed:.1f} km/h"
        )

    else:

        st.metric(
            "💨 Wind",
            "N/A"
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "EcoGuard AI • Location-based Fire & Safety Monitoring"
)

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
