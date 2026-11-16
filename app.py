import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import joblib
import random
import math
import json
import os
from datetime import datetime

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="GridShield AI",
    page_icon="🛡️",
    layout="wide"
)

# =====================================================
# PROFESSIONAL DARK THEME
# =====================================================

st.markdown("""
<style>
.stApp {
    background: #081426;
    color: #F1F5F9;
}
[data-testid="stSidebar"] {
    background: #0D1B2E;
}
[data-testid="stSidebar"] * {
    color: #F1F5F9;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: #10243D;
    border: 1px solid #234568;
    padding: 18px;
    border-radius: 12px;
}
[data-testid="stMetricValue"] { color: #38BDF8 !important; }
[data-testid="stMetricLabel"] { color: #CBD5E1 !important; }

/* Alerts: force readable text on dark backgrounds */
[data-testid="stAlert"] {
    background: #142B46 !important;
    border: 1px solid #315779 !important;
    color: #F8FAFC !important;
}
[data-testid="stAlert"] *,
[data-testid="stAlert"] p,
[data-testid="stAlert"] div,
[data-testid="stAlert"] span {
    color: #F8FAFC !important;
}

/* Distinct readable status colours */
[data-testid="stAlert"][kind="success"] {
    background: #103B32 !important;
    border-color: #00A86B !important;
}
[data-testid="stAlert"][kind="error"] {
    background: #421F2B !important;
    border-color: #FF4057 !important;
}
[data-testid="stAlert"][kind="warning"] {
    background: #44351B !important;
    border-color: #FFB020 !important;
}

/* Sidebar info message */
[data-testid="stSidebar"] [data-testid="stAlert"] {
    background: #173453 !important;
    border: 1px solid #3974A5 !important;
}

/* Select boxes and number inputs */
[data-baseweb="select"] > div,
[data-testid="stSelectbox"] [data-baseweb="select"] > div,
[data-testid="stNumberInput"] input {
    background: #173453 !important;
    border: 1px solid #3974A5 !important;
    color: #F8FAFC !important;
    -webkit-text-fill-color: #F8FAFC !important;
}
[data-baseweb="select"] *,
[data-testid="stSelectbox"] input {
    color: #F8FAFC !important;
    -webkit-text-fill-color: #F8FAFC !important;
}
[role="listbox"], [role="option"] {
    background: #173453 !important;
    color: #F8FAFC !important;
}
[role="option"]:hover {
    background: #24527A !important;
}

/* Buttons */
.stButton > button, .stDownloadButton > button {
    background: #1267C5 !important;
    color: #FFFFFF !important;
    border: 1px solid #2994FF !important;
    border-radius: 9px;
    font-weight: 600 !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background: #168BFF !important;
    color: #FFFFFF !important;
    border-color: #64B5FF !important;
}

/* General text */
h1, h2, h3, h4, p, label, [data-testid="stMarkdownContainer"] {
    color: #F1F5F9;
}
.stCaption, [data-testid="stCaption"] {
    color: #AFC3D8 !important;
}

/* High-specificity Streamlit alert overrides */
div[data-testid="stAlert"],
div[data-testid="stAlert"] > div,
div[data-testid="stAlert"] [data-testid="stMarkdownContainer"] {
    background: #142B46 !important;
    color: #FFFFFF !important;
    border-color: #315779 !important;
}
div[data-testid="stAlert"] *,
div[data-testid="stAlert"] p,
div[data-testid="stAlert"] span,
div[data-testid="stAlert"] div,
div[data-testid="stAlert"] [data-testid="stMarkdownContainer"] * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    opacity: 1 !important;
}

/* Sidebar information box */
section[data-testid="stSidebar"] div[data-testid="stAlert"],
section[data-testid="stSidebar"] div[data-testid="stAlert"] > div {
    background: #173453 !important;
    border: 1px solid #3974A5 !important;
}

/* Native Streamlit status message variants */
div[data-testid="stAlert"][kind="success"],
div[data-testid="stAlert"][kind="success"] > div {
    background: #103B32 !important;
    border-color: #00A86B !important;
}
div[data-testid="stAlert"][kind="error"],
div[data-testid="stAlert"][kind="error"] > div {
    background: #421F2B !important;
    border-color: #FF4057 !important;
}
div[data-testid="stAlert"][kind="warning"],
div[data-testid="stAlert"][kind="warning"] > div {
    background: #44351B !important;
    border-color: #FFB020 !important;
}

/* Keep selectbox labels and selected values readable */
div[data-testid="stSelectbox"] label,
div[data-testid="stSelectbox"] [data-baseweb="select"] *,
section[data-testid="stSidebar"] label {
    color: #F8FAFC !important;
    -webkit-text-fill-color: #F8FAFC !important;
}

/* GRID CONTROL sidebar styling */
section[data-testid="stSidebar"] {
    background: #0B1B30 !important;
}
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span {
    color: #F8FAFC !important;
    -webkit-text-fill-color: #F8FAFC !important;
}

section[data-testid="stSidebar"] [data-testid="stToggle"] [role="switch"] {
    background: #31506E !important;
    border: 1px solid #6B8BAA !important;
}
section[data-testid="stSidebar"] [data-testid="stToggle"] [role="switch"][aria-checked="true"] {
    background: #0284C7 !important;
    border-color: #38BDF8 !important;
}

section[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #0878D1, #0756A5) !important;
    color: #FFFFFF !important;
    border: 1px solid #38BDF8 !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    min-height: 42px !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: #0891B2 !important;
    border-color: #67E8F9 !important;
}

section[data-testid="stSidebar"] div[data-testid="stSelectbox"] [data-baseweb="select"],
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] [data-baseweb="select"] > div,
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] [role="combobox"],
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] [role="combobox"] > div {
    background: #173453 !important;
    background-color: #173453 !important;
    color: #F8FAFC !important;
    -webkit-text-fill-color: #F8FAFC !important;
    border-color: #38BDF8 !important;
}
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] [data-baseweb="select"] * {
    background-color: transparent !important;
    color: #F8FAFC !important;
    -webkit-text-fill-color: #F8FAFC !important;
}
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] [data-baseweb="select"] > div {
    border: 1px solid #38BDF8 !important;
    border-radius: 9px !important;
}
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] [data-baseweb="select"] svg {
    color: #38BDF8 !important;
    fill: #38BDF8 !important;
}
div[data-baseweb="popover"] ul,
div[data-baseweb="popover"] li,
div[data-baseweb="popover"] [role="option"] {
    background-color: #173453 !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}
div[data-baseweb="popover"] li:hover,
div[data-baseweb="popover"] [role="option"]:hover {
    background-color: #24527A !important;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD INDEPENDENT AI MODELS (CLOUD-SAFE & CACHED)
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_resource
def load_electrical_ai_model():
    try:
        model_path = os.path.join(BASE_DIR, "models", "electrical_model.pkl")
        if not os.path.exists(model_path):
            return None
        loaded = joblib.load(model_path)
        if isinstance(loaded, dict) and "model" in loaded:
            return loaded["model"]
        return loaded
    except Exception:
        return None


@st.cache_resource
def load_network_ai_model():
    try:
        model_path = os.path.join(BASE_DIR, "models", "gridshield_model.pkl")
        if not os.path.exists(model_path):
            return None
        loaded = joblib.load(model_path)
        if isinstance(loaded, dict) and "model" in loaded:
            return loaded["model"]
        return loaded
    except Exception:
        return None


electrical_model = load_electrical_ai_model()
network_model = load_network_ai_model()

# =====================================================
# SESSION STATE
# =====================================================

defaults = {
    "running": True,
    "scenario": "NORMAL",
    "history": [],
    "events": [],
    "total_analyses": 0,
    "normal_count": 0,
    "abnormal_count": 0,
    "net_packet_count": 100,
    "net_traffic_volume": 5000,
    "net_connection_rate": 20,
    "net_port_number": 80,
    "last_network_status": "Normal",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =====================================================
# ELECTRICAL AI PREDICTION HELPER
# =====================================================

ANOMALY_EXPLANATIONS = {
    "NORMAL": "All six electrical parameters are operating within nominal smart grid thresholds.",
    "OVERLOAD": "High current and load percentage exceed safe feeder capacity, causing thermal stress.",
    "VOLTAGE_DIP": "Bus voltage dropped below 10.0 kV nominal threshold, indicating voltage sag or fault.",
    "FREQUENCY_DEVIATION": "System frequency drifted outside the 49.5–50.5 Hz stability band.",
    "TRANSFORMER_OVERHEATING": "Transformer oil/winding temperature exceeded 85 °C without full current overload.",
}


def predict_electrical_condition(reading):
    """Run trained Random Forest Electrical AI on the 6 telemetry features."""
    if electrical_model is None:
        return "MODEL_UNAVAILABLE", 0.0, "Electrical AI model file not found."

    features = pd.DataFrame([{
        "voltage_kv": reading["voltage_kv"],
        "current_a": reading["current_a"],
        "frequency_hz": reading["frequency_hz"],
        "power_mw": reading["power_mw"],
        "load_percent": reading["load_percent"],
        "transformer_temp_c": reading["transformer_temp_c"],
    }])

    prediction = str(electrical_model.predict(features)[0])
    confidence = 0.0
    if hasattr(electrical_model, "predict_proba"):
        probs = electrical_model.predict_proba(features)[0]
        confidence = round(float(max(probs)) * 100.0, 1)

    explanation = ANOMALY_EXPLANATIONS.get(
        prediction,
        "Electrical AI detected an operating pattern requiring review."
    )
    return prediction, confidence, explanation


# =====================================================
# SIMULATION ENGINE
# =====================================================

def generate_reading(scenario):

    voltage = random.uniform(10.9, 11.1)
    current = random.uniform(260, 310)
    frequency = random.uniform(49.95, 50.05)
    load = random.uniform(65, 85)
    temperature = random.uniform(55, 68)
    communication = "CONNECTED"
    switching = False

    if scenario == "OVERLOAD":
        current = random.uniform(430, 480)
        load = random.uniform(115, 130)
        temperature = random.uniform(90, 105)

    elif scenario == "VOLTAGE DIP":
        voltage = random.uniform(8.5, 9.5)

    elif scenario == "FREQUENCY DEVIATION":
        frequency = random.uniform(47.5, 48.5)

    elif scenario == "TRANSFORMER OVERHEATING":
        current = random.uniform(290, 340)
        load = random.uniform(78, 92)
        temperature = random.uniform(88, 102)

    elif scenario == "COMMUNICATION ANOMALY":
        communication = "DEGRADED"

    elif scenario == "SWITCHING ANOMALY":
        switching = True

    power = round(
        voltage * current * math.sqrt(3) / 1000,
        2
    )

    reading = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "scenario": scenario,
        "voltage_kv": round(voltage, 2),
        "current_a": round(current, 2),
        "frequency_hz": round(frequency, 2),
        "power_mw": power,
        "load_percent": round(load, 2),
        "transformer_temp_c": round(temperature, 2),
        "communication_status": communication,
        "switching_event": switching
    }

    rule_alerts = detect_anomaly(reading)
    ai_condition, ai_confidence, ai_explanation = predict_electrical_condition(reading)
    ai_abnormal = ai_condition not in ("NORMAL", "MODEL_UNAVAILABLE")

    combined_alerts = list(rule_alerts)
    if ai_abnormal:
        ai_tag = f"AI: {ai_condition} ({ai_confidence:.1f}%)"
        if ai_tag not in combined_alerts:
            combined_alerts.insert(0, ai_tag)

    is_abnormal = bool(rule_alerts) or ai_abnormal

    reading["ai_condition"] = ai_condition
    reading["ai_confidence"] = ai_confidence
    reading["ai_explanation"] = ai_explanation
    reading["ai_abnormal"] = ai_abnormal
    reading["rule_alerts"] = rule_alerts
    reading["abnormal"] = is_abnormal
    reading["alerts"] = combined_alerts
    reading["breaker_status"] = (
        "OPEN - ISOLATED" if is_abnormal else "CLOSED"
    )

    return reading


# =====================================================
# RULE-BASED ELECTRICAL ANOMALY CHECKS
# =====================================================

def detect_anomaly(data):

    alerts = []

    if data["load_percent"] > 100:
        alerts.append("OVERLOAD DETECTED")

    if data["voltage_kv"] < 10:
        alerts.append("VOLTAGE ABNORMALITY")

    if not 49.5 <= data["frequency_hz"] <= 50.5:
        alerts.append("FREQUENCY DEVIATION")

    if data["transformer_temp_c"] > 85:
        alerts.append("TRANSFORMER OVERHEATING")

    if data["communication_status"] != "CONNECTED":
        alerts.append("COMMUNICATION ANOMALY")

    if data["switching_event"]:
        alerts.append("ABNORMAL SWITCHING")

    return alerts


# =====================================================
# ANIMATED GAUGE
# =====================================================

def render_gauge(title, value, maximum, unit, minimum=0):
    """Render a responsive, animated SVG gauge with value-based status colours."""

    value = float(value)
    minimum = float(minimum)
    maximum = float(maximum)
    span = max(maximum - minimum, 1e-9)
    ratio = max(0.0, min(1.0, (value - minimum) / span))

    limits = {
        "VOLTAGE": (10.0, 10.5, 11.5, 11.8),
        "CURRENT": (float("-inf"), float("-inf"), 380.0, 430.0),
        "FREQUENCY": (49.5, 49.7, 50.3, 50.5),
        "POWER": (float("-inf"), float("-inf"), 7.5, 8.5),
        "GRID LOAD": (float("-inf"), float("-inf"), 90.0, 100.0),
        "TRANSFORMER TEMP": (float("-inf"), float("-inf"), 75.0, 85.0),
    }
    critical_low, warning_low, warning_high, critical_high = limits.get(
        title.upper(),
        (float("-inf"), float("-inf"), maximum * 0.80, maximum * 0.95)
    )

    if value < critical_low or value >= critical_high:
        status, colour = "CRITICAL", "#FF4057"
    elif value < warning_low or value >= warning_high:
        status, colour = "WARNING", "#FFB020"
    else:
        status, colour = "NORMAL", "#00E676"

    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { box-sizing: border-box; }
        body {
            margin: 0; padding: 0;
            background: transparent;
            color: #F8FAFC;
            font-family: Arial, sans-serif;
        }
        .card {
            background: linear-gradient(145deg, #102A49, #0B1D34);
            border: 1px solid #285078;
            border-radius: 16px;
            padding: 12px 10px 10px;
            text-align: center;
            min-height: 224px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, .18);
        }
        .heading {
            font-size: 15px; font-weight: 700;
            color: #F8FAFC; margin: 4px 0 0;
            letter-spacing: .5px;
        }
        svg { width: 100%; max-width: 270px; display: block; margin: 0 auto; }
        .track { fill: none; stroke: #263F5D; stroke-width: 14; }
        .arc {
            fill: none; stroke: __COLOUR__; stroke-width: 14;
            stroke-linecap: round; stroke-dasharray: 377;
            stroke-dashoffset: 377;
            filter: drop-shadow(0 0 5px __COLOUR__);
            transition: stroke-dashoffset 1.1s cubic-bezier(.2,.8,.2,1);
        }
        .needle {
            stroke: #EAF6FF; stroke-width: 4; stroke-linecap: round;
            transform-origin: 150px 150px;
            transition: transform 1.1s cubic-bezier(.2,.8,.2,1);
        }
        .reading { font-size: 25px; fill: #FFFFFF; font-weight: 700; }
        .small { fill: #AFC3D8; font-size: 11px; }
        .status {
            display: inline-block; margin-top: -3px; padding: 5px 15px;
            border-radius: 20px; color: __COLOUR__;
            background: __STATUS_BG__; font-size: 11px; font-weight: 700;
            letter-spacing: .7px;
        }
    </style>
    </head>
    <body>
      <div class="card">
        <div class="heading">__TITLE__</div>
        <svg viewBox="0 0 300 190" role="img" aria-label="__TITLE__ gauge">
          <path class="track" d="M 30 150 A 120 120 0 0 1 270 150"/>
          <path class="arc" id="arc" d="M 30 150 A 120 120 0 0 1 270 150"/>
          <line class="needle" id="needle" x1="150" y1="150" x2="150" y2="52"/>
          <circle cx="150" cy="150" r="7" fill="#EAF6FF"/>
          <text x="150" y="181" text-anchor="middle" class="reading">__VALUE__</text>
          <text x="29" y="166" class="small">MIN</text>
          <text x="255" y="166" class="small">MAX</text>
        </svg>
        <div class="status">● __STATUS__</div>
      </div>
      <script>
        const ratio = __RATIO__;
        const angle = -90 + ratio * 180;
        document.getElementById("needle").style.transform = "rotate(" + angle + "deg)";
        requestAnimationFrame(() => {
          document.getElementById("arc").style.strokeDashoffset = 377 * (1 - ratio);
        });
      </script>
    </body>
    </html>
    """

    replacements = {
        "__TITLE__": title,
        "__VALUE__": f"{value:.2f} {unit}",
        "__RATIO__": json.dumps(ratio),
        "__COLOUR__": colour,
        "__STATUS__": status,
        "__STATUS_BG__": "rgba(0,230,118,.13)" if status == "NORMAL"
            else ("rgba(255,176,32,.14)" if status == "WARNING" else "rgba(255,64,87,.14)"),
    }
    for key, replacement in replacements.items():
        html_code = html_code.replace(key, replacement)

    components.html(html_code, height=245, scrolling=False)


# =====================================================
# SMART GRID TOPOLOGY
# =====================================================

def create_topology(abnormal):

    color = "#EF4444" if abnormal else "#22C55E"

    positions = [0, 2, 4, 6, 8]

    names = [
        "POWER PLANT",
        "TRANSMISSION",
        "SUBSTATION",
        "DISTRIBUTION",
        "CONSUMERS"
    ]

    fig = go.Figure()

    for i in range(4):
        fig.add_trace(go.Scatter(
            x=[positions[i], positions[i+1]],
            y=[0, 0],
            mode="lines",
            line=dict(color=color, width=6),
            showlegend=False
        ))

    fig.add_trace(go.Scatter(
        x=positions,
        y=[0] * 5,
        mode="markers+text",
        text=names,
        textposition="bottom center",
        marker=dict(
            size=23,
            color=color,
            line=dict(color="white", width=1)
        ),
        textfont=dict(color="white", size=11),
        showlegend=False
    ))

    fig.update_layout(
        title="⚡ SMART GRID ELECTRICITY FLOW",
        paper_bgcolor="#081426",
        plot_bgcolor="#081426",
        font=dict(color="white"),
        height=230,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(t=45, b=50, l=15, r=15)
    )

    return fig


# =====================================================
# HEADER
# =====================================================

st.title("🛡️ GRIDSHIELD AI")

st.subheader(
    "Intelligent Smart Grid Digital Twin & Dual-AI Security Monitoring"
)

st.caption(
    "ACADEMIC PROTOTYPE | ALL ELECTRICAL VALUES & PROTECTION ACTIONS ARE SIMULATED"
)

st.divider()


# =====================================================
# SIDEBAR CONTROLS
# =====================================================

st.sidebar.title("⚙️ GRID CONTROL")

st.session_state.running = st.sidebar.toggle(
    "Start Grid Simulation",
    value=st.session_state.running
)

scenarios = [
    "NORMAL",
    "OVERLOAD",
    "VOLTAGE DIP",
    "FREQUENCY DEVIATION",
    "TRANSFORMER OVERHEATING",
    "COMMUNICATION ANOMALY",
    "SWITCHING ANOMALY"
]

st.session_state.scenario = st.sidebar.selectbox(
    "Select Grid Scenario",
    scenarios,
    index=scenarios.index(st.session_state.scenario)
)

# AI System Status in Sidebar
st.sidebar.markdown("### 🧠 AI ENGINE STATUS")
if electrical_model is not None:
    st.sidebar.success("Electrical AI: ACTIVE")
else:
    st.sidebar.warning("Electrical AI: NOT LOADED")

if network_model is not None:
    st.sidebar.success("Network Security AI: ACTIVE")
else:
    st.sidebar.warning("Network Security AI: NOT LOADED")

st.sidebar.info(
    "Simulation only. No real electrical equipment is controlled."
)

if st.sidebar.button("🔄 RESET GRID"):

    st.session_state.history = []
    st.session_state.events = []
    st.session_state.total_analyses = 0
    st.session_state.normal_count = 0
    st.session_state.abnormal_count = 0
    st.session_state.last_network_status = "Normal"

    st.rerun()


# =====================================================
# LIVE DASHBOARD (4s CLOUD-OPTIMIZED INTERVAL)
# =====================================================

@st.fragment(run_every="4s")
def live_dashboard():

    if st.session_state.running:

        reading = generate_reading(
            st.session_state.scenario
        )

        st.session_state.history.append(reading)
        st.session_state.history = (
            st.session_state.history[-40:]
        )

        st.session_state.total_analyses += 1

        if reading["abnormal"]:

            st.session_state.abnormal_count += 1

            st.session_state.events.append({
                "Time": reading["time"],
                "AI Prediction": reading["ai_condition"],
                "Confidence": f'{reading["ai_confidence"]:.1f}%',
                "Event": ", ".join(reading["alerts"]),
                "Status": "SIMULATED PROTECTION ACTIVATED"
            })

        else:
            st.session_state.normal_count += 1

        st.session_state.events = (
            st.session_state.events[-30:]
        )

    if not st.session_state.history:

        st.info("Start simulation to generate telemetry.")
        return

    latest = st.session_state.history[-1]
    abnormal = latest["abnormal"]
    cyber_threat_active = st.session_state.last_network_status != "Normal"

    # DUAL-AI COORDINATED THREAT CORRELATION ALERT

    if abnormal and cyber_threat_active:
        st.error(
            f"🚨 CRITICAL: COORDINATED CYBER-PHYSICAL THREAT SUSPECTED! "
            f"Electrical Fault ({latest['ai_condition']}) + Cyber Threat ({st.session_state.last_network_status}) detected simultaneously."
        )
    elif abnormal:
        st.error(
            "🚨 ABNORMAL GRID CONDITION: "
            + ", ".join(latest["alerts"])
        )
    elif cyber_threat_active:
        st.warning(
            f"⚠️ ELECTRICAL GRID NOMINAL, BUT CYBER THREAT ACTIVE ({st.session_state.last_network_status}) IN NETWORK LAYER"
        )
    else:
        st.success("🟢 NORMAL GRID OPERATION — PHYSICAL & CYBER LAYERS NOMINAL")

    # TOPOLOGY

    st.plotly_chart(
        create_topology(abnormal),
        use_container_width=True,
        key="grid_topology"
    )

    # ELECTRICAL TELEMETRY

    st.subheader("📊 LIVE ELECTRICAL TELEMETRY")

    c1, c2, c3 = st.columns(3)
    c1.metric("Voltage", f'{latest["voltage_kv"]} kV')
    c2.metric("Current", f'{latest["current_a"]} A')
    c3.metric("Frequency", f'{latest["frequency_hz"]} Hz')

    c4, c5, c6 = st.columns(3)
    c4.metric("Power", f'{latest["power_mw"]} MW')
    c5.metric("Grid Load", f'{latest["load_percent"]} %')
    c6.metric("Transformer Temperature", f'{latest["transformer_temp_c"]} °C')

    # GAUGES

    st.subheader("🎯 LIVE ELECTRICAL GAUGES")
    st.caption("Simulated readings • Gauge colours change automatically with operating condition.")

    g1, g2, g3 = st.columns(3)
    with g1:
        render_gauge("VOLTAGE", latest["voltage_kv"], 12, "kV", minimum=8)
    with g2:
        render_gauge("CURRENT", latest["current_a"], 500, "A")
    with g3:
        render_gauge("FREQUENCY", latest["frequency_hz"], 55, "Hz", minimum=45)

    g4, g5, g6 = st.columns(3)
    with g4:
        render_gauge("POWER", latest["power_mw"], 12, "MW")
    with g5:
        render_gauge("GRID LOAD", latest["load_percent"], 130, "%")
    with g6:
        render_gauge("TRANSFORMER TEMP", latest["transformer_temp_c"], 110, "°C")

    # ELECTRICAL AI ANOMALY DETECTION SECTION

    st.subheader("🤖 ELECTRICAL AI ANOMALY DETECTION (RANDOM FOREST)")

    ai_cond = latest["ai_condition"]
    ai_conf = latest["ai_confidence"]
    ai_exp = latest["ai_explanation"]

    if ai_cond == "MODEL_UNAVAILABLE":
        ai_status_label = "OFFLINE"
    elif latest["ai_abnormal"]:
        ai_status_label = "CRITICAL"
    elif latest["abnormal"]:
        ai_status_label = "WARNING"
    else:
        ai_status_label = "NORMAL"

    m1, m2, m3 = st.columns(3)
    m1.metric("AI Predicted Condition", ai_cond)
    m2.metric("Prediction Confidence", f"{ai_conf:.1f} %")
    m3.metric("Electrical AI Status", ai_status_label)

    if latest["ai_abnormal"]:
        st.error(f"⚠️ Electrical AI Diagnosis: {ai_exp}")
    elif ai_cond == "MODEL_UNAVAILABLE":
        st.warning(ai_exp)
    else:
        st.success(f"✅ Electrical AI Diagnosis: {ai_exp}")

    if latest["rule_alerts"]:
        st.warning(
            "Telemetry Rule Checks: " + ", ".join(latest["rule_alerts"])
        )

    # SIMULATED AUTOMATED PROTECTION

    st.subheader("🛡️ SIMULATED AUTOMATED PROTECTION")

    p1, p2, p3 = st.columns(3)

    if abnormal:
        p1.error("RELAY: TRIGGERED (SIMULATED)")
        p2.error("BREAKER: OPEN (SIMULATED)")
        p3.warning("GRID: ISOLATED (SIMULATED)")
    else:
        p1.success("RELAY: NORMAL")
        p2.success("BREAKER: CLOSED")
        p3.success("GRID: CONNECTED")

    # HISTORY GRAPH

    st.subheader("📈 ELECTRICAL PARAMETER HISTORY")

    history = pd.DataFrame(st.session_state.history)

    chart = history.set_index("time")[
        ["voltage_kv", "frequency_hz", "load_percent"]
    ]

    st.line_chart(chart, height=280)

    # SUMMARY

    st.subheader("📊 GRID ANALYSIS SUMMARY")

    a1, a2, a3 = st.columns(3)
    a1.metric("Total Analyses", st.session_state.total_analyses)
    a2.metric("Normal Readings", st.session_state.normal_count)
    a3.metric("Abnormal Readings", st.session_state.abnormal_count)

    # EVENT HISTORY + CSV EXPORT

    st.subheader("🚨 ELECTRICAL & PROTECTION EVENT HISTORY")

    if st.session_state.events:
        events_df = pd.DataFrame(st.session_state.events)
        st.dataframe(
            events_df,
            use_container_width=True,
            hide_index=True
        )
        csv_data = events_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Grid Incident Report (CSV)",
            data=csv_data,
            file_name=f"gridshield_incident_report_{datetime.now().strftime('%H%M%S')}.csv",
            mime="text/csv",
            key="download_events_csv"
        )
    else:
        st.info("No abnormal grid events recorded yet.")

    st.caption(
        "All electrical measurements and protection actions are synthetic simulation values."
    )


live_dashboard()


# =====================================================
# SEPARATE NETWORK SECURITY MODULE
# =====================================================

st.divider()

st.header("🛡️ NETWORK SECURITY AI ANALYSIS")

st.caption(
    "Independent Random Forest network cybersecurity module (models/gridshield_model.pkl). "
    "Analyses cyber traffic patterns separately from electrical grid telemetry."
)

if network_model is not None:

    st.success("Network Security Random Forest Model Loaded & Independent")

    # 1-CLICK DEMO PRESETS FOR HACKATHON DEMONSTRATION
    st.markdown("**Quick Cyber Traffic Simulation Presets:**")
    pr1, pr2, pr3 = st.columns(3)

    if pr1.button("🟢 Load Normal Traffic Preset"):
        st.session_state.net_packet_count = 100
        st.session_state.net_traffic_volume = 5000
        st.session_state.net_connection_rate = 20
        st.session_state.net_port_number = 80
        st.rerun()

    if pr2.button("🔴 Load DoS Attack Preset"):
        st.session_state.net_packet_count = 5000
        st.session_state.net_traffic_volume = 90000
        st.session_state.net_connection_rate = 250
        st.session_state.net_port_number = 80
        st.rerun()

    if pr3.button("🟠 Load Unauthorized Access Preset"):
        st.session_state.net_packet_count = 450
        st.session_state.net_traffic_volume = 12000
        st.session_state.net_connection_rate = 95
        st.session_state.net_port_number = 22
        st.rerun()

    n1, n2, n3, n4 = st.columns(4)

    with n1:
        packet_count = st.number_input(
            "Packet Count",
            min_value=0,
            key="net_packet_count"
        )

    with n2:
        traffic_volume = st.number_input(
            "Traffic Volume",
            min_value=0,
            key="net_traffic_volume"
        )

    with n3:
        connection_rate = st.number_input(
            "Connection Rate",
            min_value=0,
            key="net_connection_rate"
        )

    with n4:
        port_number = st.number_input(
            "Port Number",
            min_value=0,
            max_value=65535,
            key="net_port_number"
        )

    if st.button("🔍 ANALYZE NETWORK TRAFFIC"):

        data = pd.DataFrame([{
            "packet_count": packet_count,
            "traffic_volume": traffic_volume,
            "connection_rate": connection_rate,
            "port_number": port_number
        }])

        prediction = str(network_model.predict(data)[0])
        st.session_state.last_network_status = prediction

        st.subheader("NETWORK SECURITY AI RESULT")

        if prediction == "Normal":
            st.success("🟢 Normal Network Traffic Detected")
        else:
            st.error(
                f"🚨 Cyber Threat Detected: {prediction}"
            )

else:
    st.warning(
        "Network model (models/gridshield_model.pkl) could not be loaded."
    )


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "GRIDSHIELD AI | Dual-AI Smart Grid Digital Twin | "
    "Academic Prototype | Simulation Only"
)
