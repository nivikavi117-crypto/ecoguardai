```python
import streamlit as st
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
from PIL import Image, ImageDraw
import random
import datetime


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="EcoGuard AI",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #0b130a;
    color: #e1e7e0;
}

.main {
    background-color: #0b130a;
}

h1, h2, h3 {
    color: #4caf50 !important;
    font-family: 'Segoe UI', sans-serif;
}

h4, h5 {
    color: #e1e7e0 !important;
}

div.stButton > button {
    background-color: #2e7d32;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 10px 24px;
    font-weight: bold;
}

div.stButton > button:hover {
    background-color: #1b5e20;
    color: white;
}

.metric-card {
    background-color: #142213;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #2e7d32;
    margin-bottom: 10px;
}

.alert-card {
    background-color: #301010;
    padding: 18px;
    border-radius: 10px;
    border: 1px solid #ff4444;
    margin-bottom: 12px;
}

.safe-card {
    background-color: #102815;
    padding: 18px;
    border-radius: 10px;
    border: 1px solid #4caf50;
    margin-bottom: 12px;
}

.info-card {
    background-color: #101d2d;
    padding: 18px;
    border-radius: 10px;
    border: 1px solid #2196f3;
    margin-bottom: 12px;
}

div[data-testid="stMetric"] {
    background-color: #142213;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #2e7d32;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "alert_sent" not in st.session_state:
    st.session_state.alert_sent = False

if "last_alert" not in st.session_state:
    st.session_state.last_alert = ""

if "system_log" not in st.session_state:
    st.session_state.system_log = []


# ============================================================
# CORE AI FUNCTIONS
# ============================================================

def predict_fire_risk(temp, humidity, wind_speed):
    """
    Simulated environmental fire-risk model.

    Higher:
        Temperature
        Wind speed

    Lower:
        Humidity
    """

    risk = (
        (temp * 1.5)
        - (humidity * 0.5)
        + (wind_speed * 0.8)
    )

    risk = max(0, min(100, risk))

    return round(risk, 2)


def get_risk_level(score):

    if score >= 75:
        return "CRITICAL", "🔴"

    elif score >= 50:
        return "HIGH", "🟠"

    elif score >= 30:
        return "MODERATE", "🟡"

    else:
        return "LOW", "🟢"


# ============================================================
# SIMULATED AI CAMERA / YOLO ENGINE
# ============================================================

def run_mock_yolo(animal_type):

    img = Image.new(
        "RGB",
        (600, 400),
        color=(30, 45, 30)
    )

    draw = ImageDraw.Draw(img)

    # Forest background
    for x in range(0, 600, 60):
        draw.rectangle(
            [x + 20, 220, x + 40, 380],
            fill=(55, 80, 45)
        )

        draw.polygon(
            [
                (x - 10, 250),
                (x + 30, 150),
                (x + 70, 250)
            ],
            fill=(35, 90, 40)
        )

    # Ground
    draw.rectangle(
        [0, 300, 600, 400],
        fill=(25, 55, 25)
    )

    # --------------------------------------------------------
    # ELEPHANT
    # --------------------------------------------------------

    if animal_type == "Elephant":

        draw.ellipse(
            [180, 140, 420, 300],
            fill=(100, 100, 100)
        )

        draw.ellipse(
            [370, 120, 470, 220],
            fill=(95, 95, 95)
        )

        draw.rectangle(
            [200, 260, 235, 350],
            fill=(90, 90, 90)
        )

        draw.rectangle(
            [350, 260, 385, 350],
            fill=(90, 90, 90)
        )

        draw.rectangle(
            [430, 180, 500, 220],
            fill=(90, 90, 90)
        )

        label = "Elephant Detected"
        confidence = random.randint(91, 98)
        distance = random.randint(150, 450)

        box = [160, 100, 510, 355]

    # --------------------------------------------------------
    # TIGER
    # --------------------------------------------------------

    elif animal_type == "Tiger":

        draw.rectangle(
            [180, 160, 420, 290],
            fill=(230, 120, 20)
        )

        draw.ellipse(
            [370, 120, 470, 210],
            fill=(200, 100, 10)
        )

        draw.rectangle(
            [210, 270, 245, 350],
            fill=(180, 90, 15)
        )

        draw.rectangle(
            [350, 270, 385, 350],
            fill=(180, 90, 15)
        )

        # Stripes
        for x in [220, 270, 320, 370]:
            draw.line(
                [x, 170, x + 25, 280],
                fill=(30, 20, 10),
                width=7
            )

        label = "Tiger Detected"
        confidence = random.randint(88, 96)
        distance = random.randint(300, 600)

        box = [160, 100, 480, 355]

    # --------------------------------------------------------
    # NO ANIMAL
    # --------------------------------------------------------

    else:

        draw.text(
            (220, 190),
            "CLEAR FOREST",
            fill=(100, 220, 100)
        )

        draw.text(
            (235, 220),
            "NO THREAT",
            fill=(100, 220, 100)
        )

        label = "No Threat"
        confidence = 0
        distance = 1500

        box = None

    # Bounding box
    if box:

        draw.rectangle(
            box,
            outline=(255, 50, 50),
            width=5
        )

        draw.rectangle(
            [box[0], box[1] - 35, box[0] + 230, box[1]],
            fill=(255, 50, 50)
        )

        draw.text(
            [box[0] + 10, box[1] - 28],
            f"{label} {confidence}%",
            fill="white"
        )

    return img, label, confidence, distance


# ============================================================
# EMERGENCY ALERT SIMULATION
# ============================================================

def send_emergency_sms(
    alert_type,
    details,
    location
):

    sms_body = (
        f"⚠️ ECOGUARD ALERT\n\n"
        f"Type: {alert_type}\n"
        f"Location: {location}\n"
        f"Details: {details}\n\n"
        f"Evacuation routes updated."
    )

    # Simulation only.
    # Real Twilio integration can be added later.

    return True, sms_body


# ============================================================
# LOG FUNCTION
# ============================================================

def add_log(message):

    timestamp = datetime.datetime.now().strftime("%H:%M:%S")

    st.session_state.system_log.append(
        f"[{timestamp}] {message}"
    )

    # Keep latest 10 logs
    st.session_state.system_log = (
        st.session_state.system_log[-10:]
    )


# ============================================================
# HEADER
# ============================================================

st.title(
    "🌲 EcoGuard AI"
)

st.markdown(
    "### Forest Safety & Disaster Prediction System"
)

st.markdown(
    "**AI-powered fire risk prediction • Wildlife detection • "
    "Emergency alerts • Safe route recommendation**"
)

st.markdown("---")


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🌲 EcoGuard AI")

st.sidebar.markdown(
    "### Interface Selection"
)

view_mode = st.sidebar.radio(
    "Select Interface View:",
    [
        "🏠 Citizen Mobile App",
        "🛡️ Department Admin Dashboard"
    ]
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    "### 🌡️ Live Environmental Telemetry"
)

input_temp = st.sidebar.slider(
    "Temperature (°C)",
    15,
    50,
    42
)

input_hum = st.sidebar.slider(
    "Humidity (%)",
    5,
    95,
    12
)

input_wind = st.sidebar.slider(
    "Wind Speed (km/h)",
    0,
    60,
    35
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    "### 📷 Simulated AI Camera"
)

selected_feed = st.sidebar.selectbox(
    "Camera Detection:",
    [
        "No Animal",
        "Elephant",
        "Tiger"
    ]
)


# ============================================================
# LOCATION
# ============================================================

# Demo location: Western Ghats region
base_lat = 11.0181
base_lon = 76.9737

village_coords = [
    11.0250,
    76.9850
]

danger_coords = [
    11.0150,
    76.9700
]

animal_coords = [
    11.0190,
    76.9780
]


# ============================================================
# AI ANALYTICS
# ============================================================

fire_risk_score = predict_fire_risk(
    input_temp,
    input_hum,
    input_wind
)

risk_level, risk_icon = get_risk_level(
    fire_risk_score
)

img_feed, ai_label, ai_conf, animal_dist = (
    run_mock_yolo(selected_feed)
)


# ============================================================
# THREAT LOGIC
# ============================================================

fire_alert = fire_risk_score >= 70

animal_alert = (
    selected_feed != "No Animal"
    and animal_dist < 500
)

system_trigger = (
    fire_alert
    or animal_alert
)


# ============================================================
# ADD SYSTEM LOGS
# ============================================================

add_log(
    f"Environmental scan completed. "
    f"Fire Risk = {fire_risk_score}%"
)

if fire_alert:

    add_log(
        "WARNING: High fire-risk condition detected."
    )

if animal_alert:

    add_log(
        f"WARNING: Wildlife intrusion detected - "
        f"{ai_label}"
    )


# ============================================================
# FIRE RISK GAUGE
# ============================================================

def create_fire_gauge(score):

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            title={
                "text": "Fire Risk Index"
            },
            gauge={
                "axis": {
                    "range": [0, 100]
                },
                "threshold": {
                    "line": {
                        "color": "red",
                        "width": 4
                    },
                    "thickness": 0.75,
                    "value": 70
                }
            }
        )
    )

    fig.update_layout(
        height=300,
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),
        paper_bgcolor="#0b130a",
        font=dict(
            color="white"
        )
    )

    return fig


# ============================================================
# MAP
# ============================================================

m = folium.Map(
    location=[
        base_lat,
        base_lon
    ],
    zoom_start=14,
    tiles="CartoDB dark_matter"
)


# Village marker

folium.Marker(
    location=village_coords,
    popup="Annamalai Village Grid",
    tooltip="Village",
    icon=folium.Icon(
        color="green",
        icon="home"
    )
).add_to(m)


# Base location

folium.Marker(
    location=[
        base_lat,
        base_lon
    ],
    popup="EcoGuard Monitoring Station",
    tooltip="Monitoring Station",
    icon=folium.Icon(
        color="blue",
        icon="info-sign"
    )
).add_to(m)


# ============================================================
# FIRE DANGER ZONE
# ============================================================

if fire_risk_score > 50:

    folium.Circle(
        location=danger_coords,
        radius=600,
        color="red",
        fill=True,
        fill_color="red",
        fill_opacity=0.35,
        popup=(
            f"🔥 Fire Hazard Zone | "
            f"Risk: {fire_risk_score}%"
        )
    ).add_to(m)


# ============================================================
# ANIMAL DETECTION MARKER
# ============================================================

if selected_feed != "No Animal":

    folium.Marker(
        location=animal_coords,
        popup=(
            f"⚠️ {ai_label} | "
            f"Confidence: {ai_conf}% | "
            f"Distance: {animal_dist}m"
        ),
        tooltip=ai_label,
        icon=folium.Icon(
            color="orange",
            icon="warning"
        )
    ).add_to(m)


# ============================================================
# ROUTES
# ============================================================

standard_route = [
    [11.0120, 76.9650],
    danger_coords,
    village_coords
]

safe_alternative_route = [
    [11.0120, 76.9650],
    [11.0300, 76.9700],
    [11.0320, 76.9820],
    village_coords
]


if system_trigger:

    # Blocked route

    folium.PolyLine(
        standard_route,
        color="red",
        weight=5,
        opacity=0.7,
        tooltip="🚫 BLOCKED HIGH-RISK ROUTE"
    ).add_to(m)

    # Safe route

    folium.PolyLine(
        safe_alternative_route,
        color="green",
        weight=7,
        opacity=0.95,
        tooltip="✅ RECOMMENDED SAFE ROUTE"
    ).add_to(m)

else:

    folium.PolyLine(
        standard_route,
        color="blue",
        weight=5,
        opacity=0.8,
        tooltip="Standard Route - Clear"
    ).add_to(m)


# ============================================================
# CITIZEN INTERFACE
# ============================================================

if view_mode == "🏠 Citizen Mobile App":

    st.subheader(
        "📱 Citizen Safety Application"
    )

    # --------------------------------------------------------
    # TOP STATUS
    # --------------------------------------------------------

    if system_trigger:

        st.error(
            "🚨 EMERGENCY EVACUATION MODE ACTIVE"
        )

    else:

        st.success(
            "✅ ALL CLEAR - ENVIRONMENT STABLE"
        )

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "🔥 Fire Risk",
            f"{fire_risk_score}%"
        )

    with c2:

        st.metric(
            "Risk Level",
            f"{risk_icon} {risk_level}"
        )

    with c3:

        st.metric(
            "🐾 Wildlife",
            ai_label
        )

    with c4:

        if system_trigger:

            st.metric(
                "System Status",
                "ALERT"
            )

        else:

            st.metric(
                "System Status",
                "SAFE"
            )

    st.markdown("---")

    # --------------------------------------------------------
    # MAP + ALERTS
    # --------------------------------------------------------

    col1, col2 = st.columns(
        [2, 1]
    )

    with col1:

        st.markdown(
            "### 🗺️ Real-Time Safe Navigation"
        )

        st_folium(
            m,
            width=None,
            height=480,
            returned_objects=[]
        )

    with col2:

        st.markdown(
            "### 🚨 Local Safety Status"
        )

        if fire_alert:

            st.markdown(
                f"""
                <div class="alert-card">
                🔥 <b>FOREST FIRE THREAT</b><br><br>
                Risk Index: <b>{fire_risk_score}%</b><br>
                Temperature: {input_temp} °C<br>
                Humidity: {input_hum}%<br>
                Wind: {input_wind} km/h
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div class="safe-card">
                🟢 <b>FIRE CONDITIONS NORMAL</b><br><br>
                Current Risk: {fire_risk_score}%
                </div>
                """,
                unsafe_allow_html=True
            )

        if animal_alert:

            st.markdown(
                f"""
                <div class="alert-card">
                🐾 <b>WILDLIFE INTRUSION</b><br><br>
                Detection: {ai_label}<br>
                Confidence: {ai_conf}%<br>
                Distance: {animal_dist} metres
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                """
                <div class="safe-card">
                🐾 <b>WILDLIFE STATUS SAFE</b><br><br>
                No immediate wildlife threat.
                </div>
                """,
                unsafe_allow_html=True
            )

        if system_trigger:

            st.success(
                "🛣️ Follow the GREEN route on the map."
            )

        else:

            st.info(
                "ℹ️ Normal movement permitted."
            )

    # --------------------------------------------------------
    # FIRE RISK GRAPH
    # --------------------------------------------------------

    st.markdown("---")

    st.markdown(
        "### 🔥 Environmental Risk Analysis"
    )

    st.plotly_chart(
        create_fire_gauge(
            fire_risk_score
        ),
        use_container_width=True
    )


# ============================================================
# ADMIN DASHBOARD
# ============================================================

else:

    st.subheader(
        "🛡️ Forest & Emergency Services Dashboard"
    )

    # --------------------------------------------------------
    # HEADER METRICS
    # --------------------------------------------------------

    m1, m2, m3, m4 = st.columns(4)

    with m1:

        st.metric(
            label="🔥 Fire Probability",
            value=f"{fire_risk_score}%",
            delta=(
                "HIGH RISK"
                if fire_alert
                else "NORMAL"
            )
        )

    with m2:

        st.metric(
            label="🌡️ Temperature",
            value=f"{input_temp} °C"
        )

    with m3:

        st.metric(
            label="🐾 AI Vision",
            value=(
                ai_label
                if selected_feed != "No Animal"
                else "No Threat"
            )
        )

    with m4:

        st.metric(
            label="🚨 Gateway",
            value=(
                "EMERGENCY"
                if system_trigger
                else "SECURE"
            )
        )

    st.markdown("---")

    # --------------------------------------------------------
    # ANALYTICS
    # --------------------------------------------------------

    col_left, col_right = st.columns(2)

    with col_left:

        st.markdown(
            "### 🔥 Fire Risk Analytics"
        )

        st.plotly_chart(
            create_fire_gauge(
                fire_risk_score
            ),
            use_container_width=True
        )

        st.markdown(
            f"""
            <div class="metric-card">
            <b>Environmental Parameters</b><br><br>
            🌡️ Temperature: {input_temp} °C<br>
            💧 Humidity: {input_hum}%<br>
            💨 Wind Speed: {input_wind} km/h<br>
            📊 Risk Level: {risk_icon} {risk_level}
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_right:

        st.markdown(
            "### 📷 AI Wildlife Detection"
        )

        st.image(
            img_feed,
            use_container_width=True
        )

        if selected_feed != "No Animal":

            st.warning(
                f"{ai_label} | "
                f"Confidence: {ai_conf}% | "
                f"Distance: {animal_dist}m"
            )

        else:

            st.success(
                "No wildlife threat detected."
            )

    st.markdown("---")

    # --------------------------------------------------------
    # MAP
    # --------------------------------------------------------

    st.markdown(
        "### 🗺️ Emergency Routing & Threat Map"
    )

    st_folium(
        m,
        width=None,
        height=500,
        returned_objects=[]
    )

    st.markdown("---")

    # --------------------------------------------------------
    # ALERT DISPATCH
    # --------------------------------------------------------

    st.markdown(
        "### 📡 Emergency Communication Center"
    )

    if system_trigger:

        st.error(
            "🚨 THREAT DETECTED — EMERGENCY DISPATCH AVAILABLE"
        )

        if st.button(
            "📨 Send Emergency Alert"
        ):

            details = (
                f"Fire Index: {fire_risk_score}%. "
                f"AI Vision: {ai_label}. "
                f"Distance: {animal_dist}m."
            )

            success, message = send_emergency_sms(
                "CRITICAL FOREST THREAT",
                details,
                f"Grid [{base_lat:.4f}, {base_lon:.4f}]"
            )

            if success:

                st.session_state.alert_sent = True
                st.session_state.last_alert = message

                add_log(
                    "Emergency alert dispatched successfully."
                )

                st.success(
                    "✅ Emergency alert simulated successfully!"
                )

                st.code(
                    message,
                    language="text"
                )

    else:

        st.success(
            "🟢 No emergency dispatch required."
        )

    # --------------------------------------------------------
    # SYSTEM LOG
    # --------------------------------------------------------

    st.markdown("---")

    st.markdown(
        "### 📋 System Operations Log"
    )

    if st.session_state.system_log:

        log_text = "\n".join(
            st.session_state.system_log
        )

    else:

        log_text = (
            "System initialized successfully."
        )

    st.text_area(
        "Live Audit Feed",
        value=log_text,
        height=180
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#777;">
    🌲 <b>EcoGuard AI</b> |
    AI-Powered Forest Safety & Disaster Prediction |
    Every Second Protects a Life
    </div>
    """,
    unsafe_allow_html=True
)
```
