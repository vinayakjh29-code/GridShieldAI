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
import time
from datetime import datetime

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="GridShield AI | Smart Grid Digital Twin",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# HIGH-CONTRAST DARK COMMAND CENTER CSS (NO WHITE BOXES!)
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.stApp {
    background: radial-gradient(circle at 18% 8%, #0E2442 0%, #060E1C 50%, #030711 100%) !important;
    color: #F8FAFC !important;
}

header[data-testid="stHeader"] {
    background: rgba(6, 14, 28, 0.85) !important;
}

/* Sidebar Dark Background */
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div {
    background: #081224 !important;
    border-right: 1px solid rgba(56, 189, 248, 0.2);
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span {
    color: #F8FAFC !important;
}

/* Fix Selectbox & Number Input White Backgrounds */
div[data-baseweb="select"] > div,
div[data-baseweb="base-input"],
div[data-baseweb="input"] > div,
input {
    background-color: #13294B !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    border: 1px solid #38BDF8 !important;
    border-radius: 10px !important;
}
div[data-baseweb="select"] span,
div[data-baseweb="select"] div {
    background-color: transparent !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}
div[data-baseweb="popover"] ul,
div[data-baseweb="popover"] li,
ul[role="listbox"],
li[role="option"] {
    background-color: #13294B !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}
li[role="option"]:hover {
    background-color: #1E40AF !important;
}

/* Fix ALL Streamlit Alert / Info / Success / Error Boxes (No White Boxes) */
div[data-testid="stAlert"],
div[data-testid="stNotification"],
[role="alert"] {
    background-color: #112645 !important;
    border: 1px solid #38BDF8 !important;
    border-radius: 12px !important;
    color: #FFFFFF !important;
}
div[data-testid="stAlert"] *,
div[data-testid="stNotification"] *,
[role="alert"] * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

/* Animated Hero Banner */
@keyframes pulseRing {
    0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
    70% { box-shadow: 0 0 0 9px rgba(16, 185, 129, 0); }
    100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

.hero-banner {
    background: linear-gradient(135deg, #0F2547 0%, #081326 100%);
    border: 1px solid rgba(56, 189, 248, 0.35);
    border-radius: 18px;
    padding: 20px 26px;
    margin-bottom: 14px;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.45);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
}
.hero-title {
    font-size: 28px;
    font-weight: 800;
    color: #38BDF8;
    margin: 0;
}
.hero-sub {
    color: #CBD5E1;
    font-size: 13.5px;
    margin: 4px 0 0 0;
    font-weight: 500;
}
.live-pill {
    display: inline-flex;
    align-items: center;
    gap: 9px;
    background: rgba(16, 185, 129, 0.16);
    border: 1px solid #10B981;
    color: #34D399;
    padding: 8px 16px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.7px;
}
.pulse-dot {
    width: 9px;
    height: 9px;
    background: #10B981;
    border-radius: 50%;
    animation: pulseRing 1.8s infinite;
}

/* 3-Step Concept Strip */
.concept-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 12px;
    margin-bottom: 16px;
}
.concept-card {
    background: #0D1D38;
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 13px;
    padding: 12px 16px;
    display: flex;
    align-items: center;
    gap: 12px;
}
.concept-icon {
    font-size: 22px;
    background: rgba(56, 189, 248, 0.14);
    border: 1px solid rgba(56, 189, 248, 0.35);
    border-radius: 10px;
    width: 42px;
    height: 42px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.concept-title {
    font-size: 12px;
    font-weight: 700;
    color: #38BDF8;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}
.concept-desc {
    font-size: 12px;
    color: #E2E8F0;
    margin-top: 2px;
}

/* Status Banner */
.status-banner {
    padding: 14px 20px;
    border-radius: 12px;
    font-weight: 700;
    font-size: 14px;
    margin-bottom: 14px;
    border: 1px solid;
}
.status-ok {
    background: rgba(6, 78, 59, 0.75);
    border-color: #10B981;
    color: #ECFDF5;
}
.status-warn {
    background: rgba(120, 53, 15, 0.8);
    border-color: #F59E0B;
    color: #FFFBEB;
}
.status-crit {
    background: rgba(136, 19, 55, 0.85);
    border-color: #F43F5E;
    color: #FFF1F2;
}

/* Section Labels */
.section-label {
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: #38BDF8;
    margin: 18px 0 10px 0;
}

/* Metric Cards */
[data-testid="stMetric"] {
    background: #0E1F3D !important;
    border: 1px solid rgba(56, 189, 248, 0.25) !important;
    border-radius: 14px !important;
    padding: 14px 16px !important;
}
[data-testid="stMetricLabel"] {
    color: #94A3B8 !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    text-transform: uppercase;
}
[data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    color: #FFFFFF !important;
    font-size: 22px !important;
    font-weight: 700 !important;
}

/* Buttons */
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(135deg, #0284C7 0%, #2563EB 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid #38BDF8 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}
section[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD INDEPENDENT AI MODELS
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_resource
def load_electrical_ai_model():
    try:
        model_path = os.path.join(BASE_DIR, "models", "electrical_model.pkl")
        if not os.path.exists(model_path):
            return None
        loaded = joblib.load(model_path)
        return loaded["model"] if isinstance(loaded, dict) and "model" in loaded else loaded
    except Exception:
        return None


@st.cache_resource
def load_network_ai_model():
    try:
        model_path = os.path.join(BASE_DIR, "models", "gridshield_model.pkl")
        if not os.path.exists(model_path):
            return None
        loaded = joblib.load(model_path)
        return loaded["model"] if isinstance(loaded, dict) and "model" in loaded else loaded
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

    power = round(voltage * current * math.sqrt(3) / 1000, 2)

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
    reading["breaker_status"] = "OPEN - ISOLATED" if is_abnormal else "CLOSED"

    return reading


# =====================================================
# LIVE ANIMATED ELECTRICITY FLOW TOPOLOGY
# =====================================================

def render_animated_topology(abnormal, power_mw, load_pct):
    if abnormal:
        flow_color = "#F43F5E"
        status_text = "FAULT ISOLATED • BREAKER OPEN"
        pulse_speed = "0s"
        pulse_opacity = "0"
        breaker_angle = "-38"
        sub_glow = "rgba(244, 63, 94, 0.35)"
    else:
        flow_color = "#10B981"
        status_text = f"ENERGIZED • {power_mw:.2f} MW FLOWING ({load_pct:.0f}% LOAD)"
        pulse_speed = "1.5s"
        pulse_opacity = "1"
        breaker_angle = "0"
        sub_glow = "rgba(16, 185, 129, 0.28)"

    html_topo = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ background: transparent; font-family: Arial, sans-serif; color: #F8FAFC; }}
        .topo-box {{
            background: #0C1B33;
            border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 16px;
            padding: 14px 18px 10px;
        }}
        .topo-header {{
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 6px; flex-wrap: wrap; gap: 8px;
        }}
        .topo-title {{ font-size: 12px; font-weight: 700; color: #38BDF8; letter-spacing: 1px; }}
        .topo-badge {{
            font-size: 11px; font-weight: 700;
            color: {flow_color};
            background: {sub_glow};
            border: 1px solid {flow_color};
            padding: 4px 12px; border-radius: 999px;
        }}
        svg {{ width: 100%; height: 140px; display: block; }}
        .grid-line {{ stroke: {flow_color}; stroke-width: 4; stroke-opacity: 0.35; }}
        .energy-pulse {{
            stroke: #38BDF8; stroke-width: 5; stroke-linecap: round;
            stroke-dasharray: 18 42; opacity: {pulse_opacity};
            animation: flowMove {pulse_speed} linear infinite;
        }}
        @keyframes flowMove {{
            from {{ stroke-dashoffset: 120; }}
            to {{ stroke-dashoffset: 0; }}
        }}
        .node-circle {{ fill: #0B172E; stroke: {flow_color}; stroke-width: 3.5; }}
        .node-label {{ fill: #FFFFFF; font-size: 11px; font-weight: 700; }}
        .node-sub {{ fill: #94A3B8; font-size: 9.5px; }}
    </style>
    </head>
    <body>
      <div class="topo-box">
        <div class="topo-header">
            <div class="topo-title">⚡ LIVE SMART GRID POWER FLOW &amp; BREAKER DIGITAL TWIN</div>
            <div class="topo-badge">● {status_text}</div>
        </div>
        <svg viewBox="0 0 920 140">
          <line class="grid-line" x1="100" y1="58" x2="290" y2="58"/>
          <line class="energy-pulse" x1="100" y1="58" x2="290" y2="58"/>
          <line class="grid-line" x1="290" y1="58" x2="460" y2="58"/>
          <line class="energy-pulse" x1="290" y1="58" x2="460" y2="58"/>
          <line class="grid-line" x1="460" y1="58" x2="530" y2="58"/>
          <line x1="530" y1="58" x2="585" y2="58" stroke="{flow_color}" stroke-width="5"
                stroke-linecap="round" transform="rotate({breaker_angle} 530 58)"/>
          <text x="557" y="32" text-anchor="middle" fill="{flow_color}" font-size="10" font-weight="700">
            {"BREAKER OPEN" if abnormal else "BREAKER CLOSED"}
          </text>
          <line class="grid-line" x1="585" y1="58" x2="660" y2="58"/>
          <line class="energy-pulse" x1="585" y1="58" x2="660" y2="58"/>
          <line class="grid-line" x1="660" y1="58" x2="830" y2="58"/>
          <line class="energy-pulse" x1="660" y1="58" x2="830" y2="58"/>

          <g transform="translate(100,58)">
            <circle class="node-circle" r="23"/>
            <text y="5" text-anchor="middle" font-size="15">🏭</text>
            <text y="42" text-anchor="middle" class="node-label">POWER PLANT</text>
            <text y="56" text-anchor="middle" class="node-sub">11 kV Gen</text>
          </g>
          <g transform="translate(290,58)">
            <circle class="node-circle" r="23"/>
            <text y="5" text-anchor="middle" font-size="15">🗼</text>
            <text y="42" text-anchor="middle" class="node-label">TRANSMISSION</text>
            <text y="56" text-anchor="middle" class="node-sub">HV Bus</text>
          </g>
          <g transform="translate(460,58)">
            <circle class="node-circle" r="25"/>
            <text y="5" text-anchor="middle" font-size="16">🤖</text>
            <text y="42" text-anchor="middle" class="node-label">AI SUBSTATION</text>
            <text y="56" text-anchor="middle" class="node-sub">Dual-AI Guard</text>
          </g>
          <g transform="translate(660,58)">
            <circle class="node-circle" r="23"/>
            <text y="5" text-anchor="middle" font-size="15">🔌</text>
            <text y="42" text-anchor="middle" class="node-label">DISTRIBUTION</text>
            <text y="56" text-anchor="middle" class="node-sub">Feeder Line</text>
          </g>
          <g transform="translate(830,58)">
            <circle class="node-circle" r="23"/>
            <text y="5" text-anchor="middle" font-size="15">🏙️</text>
            <text y="42" text-anchor="middle" class="node-label">CONSUMERS</text>
            <text y="56" text-anchor="middle" class="node-sub">Smart Load</text>
          </g>
        </svg>
      </div>
    </body>
    </html>
    """
    components.html(html_topo, height=192, scrolling=False)


# =====================================================
# SMOOTH-MOTION ANIMATED METER GAUGE
# =====================================================

def render_gauge(title, value, prev_value, maximum, unit, safe_hint, minimum=0):
    value = float(value)
    prev_value = float(prev_value)
    minimum = float(minimum)
    maximum = float(maximum)
    span = max(maximum - minimum, 1e-9)

    ratio = max(0.0, min(1.0, (value - minimum) / span))
    prev_ratio = max(0.0, min(1.0, (prev_value - minimum) / span))

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
        status, colour, bg_pill = "CRITICAL", "#F43F5E", "rgba(244, 63, 94, 0.18)"
    elif value < warning_low or value >= warning_high:
        status, colour, bg_pill = "WARNING", "#F59E0B", "rgba(245, 158, 11, 0.18)"
    else:
        status, colour, bg_pill = "NORMAL", "#10B981", "rgba(16, 185, 129, 0.18)"

    start_angle = -90 + (prev_ratio * 180)
    start_offset = 377 * (1 - prev_ratio)

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        * {{ box-sizing: border-box; }}
        body {{ margin: 0; padding: 0; background: transparent; color: #F8FAFC; font-family: Arial, sans-serif; }}
        .card {{
            background: #0D1E3B;
            border: 1px solid rgba(56, 189, 248, 0.28);
            border-radius: 16px;
            padding: 12px 10px 10px;
            text-align: center;
            min-height: 230px;
        }}
        .heading {{ font-size: 12px; font-weight: 700; color: #FFFFFF; letter-spacing: 0.8px; }}
        .hint {{ font-size: 10px; color: #94A3B8; margin-top: 2px; }}
        svg {{ width: 100%; max-width: 250px; display: block; margin: 0 auto; }}
        .track {{ fill: none; stroke: #1E3A5F; stroke-width: 13; stroke-linecap: round; }}
        .arc {{
            fill: none; stroke: {colour}; stroke-width: 13;
            stroke-linecap: round; stroke-dasharray: 377;
            stroke-dashoffset: {start_offset};
            transition: stroke-dashoffset 1.1s ease-out;
        }}
        .needle {{
            stroke: #FFFFFF; stroke-width: 3.5; stroke-linecap: round;
            transform-origin: 150px 150px;
            transform: rotate({start_angle}deg);
            transition: transform 1.1s ease-out;
        }}
        .reading {{ font-size: 22px; fill: #FFFFFF; font-weight: 700; }}
        .small {{ fill: #94A3B8; font-size: 10px; font-weight: 600; }}
        .status {{
            display: inline-block; margin-top: 2px; padding: 4px 13px;
            border-radius: 999px; color: {colour};
            border: 1px solid {colour};
            background: {bg_pill}; font-size: 10.5px; font-weight: 700;
        }}
    </style>
    </head>
    <body>
      <div class="card">
        <div class="heading">{title}</div>
        <div class="hint">Safe Range: {safe_hint}</div>
        <svg viewBox="0 0 300 186">
          <path class="track" d="M 30 150 A 120 120 0 0 1 270 150"/>
          <path class="arc" id="arc" d="M 30 150 A 120 120 0 0 1 270 150"/>
          <line class="needle" id="needle" x1="150" y1="150" x2="150" y2="54"/>
          <circle cx="150" cy="150" r="7" fill="#38BDF8"/>
          <text x="150" y="180" text-anchor="middle" class="reading">{value:.2f} {unit}</text>
          <text x="26" y="168" class="small">MIN</text>
          <text x="252" y="168" class="small">MAX</text>
        </svg>
        <div class="status">● {status}</div>
      </div>
      <script>
        const targetAngle = -90 + ({ratio} * 180);
        const targetOffset = 377 * (1 - {ratio});
        setTimeout(() => {{
          document.getElementById("needle").style.transform = "rotate(" + targetAngle + "deg)";
          document.getElementById("arc").style.strokeDashoffset = targetOffset;
        }}, 50);
      </script>
    </body>
    </html>
    """
    components.html(html_code, height=244, scrolling=False)


# =====================================================
# HEADER & 3-STEP CONCEPT CLARITY STRIP
# =====================================================

st.markdown("""
<div class="hero-banner">
    <div>
        <h1 class="hero-title">🛡️ GRIDSHIELD AI</h1>
        <p class="hero-sub">Real-Time Smart Grid Digital Twin • Dual-AI Physical &amp; Cybersecurity Protection</p>
    </div>
    <div class="live-pill">
        <span class="pulse-dot"></span> LIVE DIGITAL TWIN ACTIVE
    </div>
</div>

<div class="concept-grid">
    <div class="concept-card">
        <div class="concept-icon">⚡</div>
        <div>
            <div class="concept-title">1. Physical Grid Sensors</div>
            <div class="concept-desc">Monitors Voltage, Current, Frequency, Load &amp; Temp in real time.</div>
        </div>
    </div>
    <div class="concept-card">
        <div class="concept-icon">🧠</div>
        <div>
            <div class="concept-title">2. Dual-AI Threat Brain</div>
            <div class="concept-desc">2 Random Forest AIs detect electrical faults &amp; cyber-attacks simultaneously.</div>
        </div>
    </div>
    <div class="concept-card">
        <div class="concept-icon">🛡️</div>
        <div>
            <div class="concept-title">3. Auto-Breaker Isolation</div>
            <div class="concept-desc">Trips relay &amp; isolates substation instantly to prevent blackouts.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# =====================================================
# SIDEBAR CONTROLS (HIGH CONTRAST DARK CARDS)
# =====================================================

st.sidebar.markdown("## ⚙️ GRID CONTROL PANEL")

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
    "Inject Grid Fault Scenario",
    scenarios,
    index=scenarios.index(st.session_state.scenario)
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🧠 AI ENGINE STATUS")

elec_badge = "ACTIVE ✅" if electrical_model is not None else "OFFLINE ⚠️"
net_badge = "ACTIVE ✅" if network_model is not None else "OFFLINE ⚠️"

st.sidebar.markdown(f"""
<div style="background:#112645; border:1px solid #10B981; border-radius:10px; padding:10px 12px; margin-bottom:8px; color:#FFFFFF; font-size:13px; font-weight:600;">
    ⚡ Electrical AI: {elec_badge}
</div>
<div style="background:#112645; border:1px solid #10B981; border-radius:10px; padding:10px 12px; margin-bottom:10px; color:#FFFFFF; font-size:13px; font-weight:600;">
    🛡️ Network Security AI: {net_badge}
</div>
<div style="background:#0F213D; border:1px solid #38BDF8; border-radius:10px; padding:10px 12px; margin-bottom:12px; color:#CBD5E1; font-size:12px;">
    Academic Prototype • All electrical values &amp; breaker trips are simulated.
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("🔄 RESET GRID"):
    st.session_state.history = []
    st.session_state.events = []
    st.session_state.total_analyses = 0
    st.session_state.normal_count = 0
    st.session_state.abnormal_count = 0
    st.session_state.last_network_status = "Normal"
    st.rerun()


# =====================================================
# GENERATE LIVE READING
# =====================================================

if st.session_state.running or not st.session_state.history:
    reading = generate_reading(st.session_state.scenario)
    st.session_state.history.append(reading)
    st.session_state.history = st.session_state.history[-40:]
    st.session_state.total_analyses += 1

    if reading["abnormal"]:
        st.session_state.abnormal_count += 1
        st.session_state.events.append({
            "Time": reading["time"],
            "AI Prediction": reading["ai_condition"],
            "Confidence": f'{reading["ai_confidence"]:.1f}%',
            "Event": ", ".join(reading["alerts"]),
            "Status": "BREAKER ISOLATED"
        })
    else:
        st.session_state.normal_count += 1

    st.session_state.events = st.session_state.events[-30:]

latest = st.session_state.history[-1]
previous = st.session_state.history[-2] if len(st.session_state.history) > 1 else latest
abnormal = latest["abnormal"]
cyber_threat_active = st.session_state.last_network_status != "Normal"

# STATUS BANNER
if abnormal and cyber_threat_active:
    st.markdown(
        f'<div class="status-banner status-crit">🚨 CRITICAL: COORDINATED CYBER-PHYSICAL ATTACK DETECTED! '
        f'Physical Fault ({latest["ai_condition"]}) + Cyber Threat ({st.session_state.last_network_status}) occurring simultaneously.</div>',
        unsafe_allow_html=True
    )
elif abnormal:
    st.markdown(
        f'<div class="status-banner status-crit">🚨 PHYSICAL GRID FAULT DETECTED: {" • ".join(latest["alerts"])}</div>',
        unsafe_allow_html=True
    )
elif cyber_threat_active:
    st.markdown(
        f'<div class="status-banner status-warn">⚠️ ELECTRICAL GRID NORMAL — CYBER THREAT ACTIVE ({st.session_state.last_network_status}) IN NETWORK LAYER</div>',
        unsafe_allow_html=True
    )
else:
    st.markdown(
        '<div class="status-banner status-ok">🟢 SYSTEM HEALTHY — PHYSICAL POWER GRID &amp; CYBER NETWORK SECURE</div>',
        unsafe_allow_html=True
    )

# ANIMATED POWER FLOW TOPOLOGY
render_animated_topology(abnormal, latest["power_mw"], latest["load_percent"])

# LIVE TELEMETRY METRICS
st.markdown('<div class="section-label">📊 LIVE ELECTRICAL TELEMETRY</div>', unsafe_allow_html=True)

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Voltage", f'{latest["voltage_kv"]} kV')
c2.metric("Current", f'{latest["current_a"]} A')
c3.metric("Frequency", f'{latest["frequency_hz"]} Hz')
c4.metric("Power", f'{latest["power_mw"]} MW')
c5.metric("Grid Load", f'{latest["load_percent"]} %')
c6.metric("Transformer Temp", f'{latest["transformer_temp_c"]} °C')

# SMOOTH-MOTION GAUGES
st.markdown('<div class="section-label">🎯 LIVE MOTION INSTRUMENTATION METERS</div>', unsafe_allow_html=True)

g1, g2, g3 = st.columns(3)
with g1:
    render_gauge("VOLTAGE", latest["voltage_kv"], previous["voltage_kv"], 12, "kV", "10.5 – 11.5 kV", minimum=8)
with g2:
    render_gauge("CURRENT", latest["current_a"], previous["current_a"], 500, "A", "< 380 A")
with g3:
    render_gauge("FREQUENCY", latest["frequency_hz"], previous["frequency_hz"], 55, "Hz", "49.5 – 50.5 Hz", minimum=45)

g4, g5, g6 = st.columns(3)
with g4:
    render_gauge("POWER", latest["power_mw"], previous["power_mw"], 12, "MW", "< 7.5 MW")
with g5:
    render_gauge("GRID LOAD", latest["load_percent"], previous["load_percent"], 130, "%", "< 90 %")
with g6:
    render_gauge("TRANSFORMER TEMP", latest["transformer_temp_c"], previous["transformer_temp_c"], 110, "°C", "< 75 °C")

# ELECTRICAL AI DIAGNOSIS & PROTECTION
st.markdown('<div class="section-label">🤖 ELECTRICAL AI ANOMALY DETECTION &amp; AUTOMATED PROTECTION</div>', unsafe_allow_html=True)

ai_cond = latest["ai_condition"]
ai_conf = latest["ai_confidence"]
ai_exp = latest["ai_explanation"]

m1, m2, m3, m4 = st.columns(4)
m1.metric("AI Predicted Condition", ai_cond)
m2.metric("Prediction Confidence", f"{ai_conf:.1f} %")
m3.metric("Protection Relay", "TRIGGERED" if abnormal else "NORMAL")
m4.metric("Circuit Breaker", "OPEN (ISOLATED)" if abnormal else "CLOSED")

diag_class = "status-crit" if latest["ai_abnormal"] else "status-ok"
diag_icon = "⚠️" if latest["ai_abnormal"] else "✅"
st.markdown(f'<div class="status-banner {diag_class}">{diag_icon} Electrical AI Diagnosis: {ai_exp}</div>', unsafe_allow_html=True)

# TELEMETRY HISTORY GRAPH
st.markdown('<div class="section-label">📈 ELECTRICAL PARAMETER HISTORY</div>', unsafe_allow_html=True)

history_df = pd.DataFrame(st.session_state.history)
trend_fig = go.Figure()
trend_fig.add_trace(go.Scatter(
    x=history_df["time"], y=history_df["load_percent"],
    name="Grid Load (%)", mode="lines+markers",
    line=dict(color="#38BDF8", width=2.5, shape="spline")
))
trend_fig.add_trace(go.Scatter(
    x=history_df["time"], y=history_df["frequency_hz"],
    name="Frequency (Hz)", mode="lines",
    line=dict(color="#10B981", width=2.2, shape="spline")
))
trend_fig.add_trace(go.Scatter(
    x=history_df["time"], y=history_df["voltage_kv"],
    name="Voltage (kV)", mode="lines",
    line=dict(color="#A78BFA", width=2.2, shape="spline")
))
trend_fig.update_layout(
    paper_bgcolor="#0C1B33",
    plot_bgcolor="#0C1B33",
    font=dict(color="#FFFFFF"),
    height=250,
    margin=dict(t=25, b=30, l=20, r=20),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis=dict(showgrid=False),
    yaxis=dict(gridcolor="rgba(148, 163, 184, 0.15)")
)
st.plotly_chart(trend_fig, use_container_width=True)

# SUMMARY & EVENT LOG
st.markdown('<div class="section-label">🚨 GRID ANALYSIS SUMMARY &amp; EVENT HISTORY</div>', unsafe_allow_html=True)

a1, a2, a3 = st.columns(3)
a1.metric("Total Analyses", st.session_state.total_analyses)
a2.metric("Normal Readings", st.session_state.normal_count)
a3.metric("Abnormal Readings", st.session_state.abnormal_count)

if st.session_state.events:
    events_df = pd.DataFrame(st.session_state.events)
    st.dataframe(events_df, use_container_width=True, hide_index=True)
    csv_data = events_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Grid Incident Report (CSV)",
        data=csv_data,
        file_name=f"gridshield_incident_report_{datetime.now().strftime('%H%M%S')}.csv",
        mime="text/csv"
    )
else:
    st.markdown('<div class="status-banner status-ok">No abnormal grid events recorded yet.</div>', unsafe_allow_html=True)

# =====================================================
# SEPARATE NETWORK SECURITY MODULE
# =====================================================

st.divider()
st.markdown('<div class="section-label">🛡️ NETWORK SECURITY AI ANALYSIS (INDEPENDENT CYBER ENGINE)</div>', unsafe_allow_html=True)

if network_model is not None:
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
        packet_count = st.number_input("Packet Count", min_value=0, key="net_packet_count")
    with n2:
        traffic_volume = st.number_input("Traffic Volume", min_value=0, key="net_traffic_volume")
    with n3:
        connection_rate = st.number_input("Connection Rate", min_value=0, key="net_connection_rate")
    with n4:
        port_number = st.number_input("Port Number", min_value=0, max_value=65535, key="net_port_number")

    if st.button("🔍 ANALYZE NETWORK TRAFFIC"):
        data = pd.DataFrame([{
            "packet_count": packet_count,
            "traffic_volume": traffic_volume,
            "connection_rate": connection_rate,
            "port_number": port_number
        }])
        prediction = str(network_model.predict(data)[0])
        st.session_state.last_network_status = prediction

        if prediction == "Normal":
            st.markdown('<div class="status-banner status-ok">🟢 Normal Network Traffic Detected</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="status-banner status-crit">🚨 Cyber Threat Detected: {prediction}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="status-banner status-warn">Network model (models/gridshield_model.pkl) could not be loaded.</div>', unsafe_allow_html=True)

st.divider()
st.caption("GRIDSHIELD AI | Dual-AI Smart Grid Digital Twin | Academic Prototype | Simulation Only")

# AUTO-REFRESH EVERY 3.5 SECONDS WHEN RUNNING
if st.session_state.running:
    time.sleep(3.5)
    st.rerun()
