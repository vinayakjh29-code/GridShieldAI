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
    page_title="GridShield AI | Smart Grid Digital Twin",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# MODERN COMMAND CENTER THEME & MOTION STYLES
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.stApp {
    background: radial-gradient(circle at 18% 8%, #0E2442 0%, #060E1C 50%, #030711 100%);
    color: #F8FAFC;
}

header[data-testid="stHeader"] {
    background: rgba(6, 14, 28, 0.78) !important;
    backdrop-filter: blur(12px);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #091528 0%, #040A14 100%) !important;
    border-right: 1px solid rgba(56, 189, 248, 0.18);
}
section[data-testid="stSidebar"] * {
    color: #F1F5F9 !important;
}

/* Animated Hero Banner */
@keyframes pulseRing {
    0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
    70% { box-shadow: 0 0 0 9px rgba(16, 185, 129, 0); }
    100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

.hero-banner {
    background: linear-gradient(135deg, rgba(15, 36, 66, 0.88) 0%, rgba(8, 18, 36, 0.94) 100%);
    border: 1px solid rgba(56, 189, 248, 0.28);
    border-radius: 18px;
    padding: 20px 26px;
    margin-bottom: 14px;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(14px);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
}
.hero-title {
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -0.5px;
    background: linear-gradient(90deg, #FFFFFF 0%, #38BDF8 55%, #34D399 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.hero-sub {
    color: #94A3B8;
    font-size: 13.5px;
    margin: 4px 0 0 0;
    font-weight: 500;
}
.live-pill {
    display: inline-flex;
    align-items: center;
    gap: 9px;
    background: rgba(16, 185, 129, 0.14);
    border: 1px solid rgba(16, 185, 129, 0.45);
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

/* 3-Step Concept Strip for Instant Judge Clarity */
.concept-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 12px;
    margin-bottom: 16px;
}
.concept-card {
    background: rgba(13, 27, 50, 0.72);
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-radius: 13px;
    padding: 12px 16px;
    display: flex;
    align-items: center;
    gap: 12px;
}
.concept-icon {
    font-size: 22px;
    background: rgba(56, 189, 248, 0.12);
    border: 1px solid rgba(56, 189, 248, 0.3);
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
    color: #CBD5E1;
    margin-top: 2px;
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

/* Glassmorphic Metric Cards */
[data-testid="stMetric"] {
    background: rgba(14, 29, 54, 0.72) !important;
    border: 1px solid rgba(56, 189, 248, 0.2) !important;
    border-radius: 14px !important;
    padding: 14px 16px !important;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
    transition: transform 0.2s ease, border-color 0.2s ease;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    border-color: rgba(56, 189, 248, 0.5) !important;
}
[data-testid="stMetricLabel"] {
    color: #94A3B8 !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}
[data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    color: #F8FAFC !important;
    font-size: 22px !important;
    font-weight: 700 !important;
}

/* Status Alerts */
div[data-testid="stAlert"],
div[data-testid="stAlert"] > div {
    border-radius: 12px !important;
    border-width: 1px !important;
    font-weight: 600 !important;
}
div[data-testid="stAlert"] *,
div[data-testid="stAlert"] p,
div[data-testid="stAlert"] span {
    color: #F8FAFC !important;
    -webkit-text-fill-color: #F8FAFC !important;
}
div[data-testid="stAlert"][kind="success"],
div[data-testid="stAlert"][kind="success"] > div {
    background: rgba(6, 78, 59, 0.6) !important;
    border-color: rgba(16, 185, 129, 0.55) !important;
}
div[data-testid="stAlert"][kind="error"],
div[data-testid="stAlert"][kind="error"] > div {
    background: rgba(127, 29, 29, 0.62) !important;
    border-color: rgba(244, 63, 94, 0.6) !important;
}
div[data-testid="stAlert"][kind="warning"],
div[data-testid="stAlert"][kind="warning"] > div {
    background: rgba(120, 53, 15, 0.6) !important;
    border-color: rgba(245, 158, 11, 0.55) !important;
}

/* Inputs & Dropdowns */
[data-baseweb="select"] > div,
[data-testid="stSelectbox"] [data-baseweb="select"] > div,
[data-testid="stNumberInput"] input {
    background: rgba(15, 31, 56, 0.9) !important;
    border: 1px solid rgba(56, 189, 248, 0.35) !important;
    border-radius: 10px !important;
    color: #F8FAFC !important;
    -webkit-text-fill-color: #F8FAFC !important;
}
div[data-baseweb="popover"] ul,
div[data-baseweb="popover"] li,
div[data-baseweb="popover"] [role="option"] {
    background-color: #0F1F38 !important;
    color: #F8FAFC !important;
    -webkit-text-fill-color: #F8FAFC !important;
}
div[data-baseweb="popover"] li:hover,
div[data-baseweb="popover"] [role="option"]:hover {
    background-color: #1E3A5F !important;
}

/* Buttons */
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(135deg, #0284C7 0%, #2563EB 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(125, 211, 252, 0.4) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 14px rgba(2, 132, 199, 0.32);
    transition: all 0.2s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background: linear-gradient(135deg, #0EA5E9 0%, #3B82F6 100%) !important;
    transform: translateY(-1px);
}
section[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
}
section[data-testid="stSidebar"] [data-testid="stToggle"] [role="switch"][aria-checked="true"] {
    background: #0EA5E9 !important;
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
# LIVE ANIMATED ELECTRICITY FLOW TOPOLOGY (SVG MOTION)
# =====================================================

def render_animated_topology(abnormal, power_mw, load_pct):
    """Animated SVG power grid flow diagram showing moving electricity pulses and breaker state."""
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
        pulse_speed = "1.6s"
        pulse_opacity = "1"
        breaker_angle = "0"
        sub_glow = "rgba(16, 185, 129, 0.28)"

    html_topo = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@600;700&family=JetBrains+Mono:wght@600;700&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ background: transparent; font-family: 'Inter', sans-serif; color: #F8FAFC; }}
        .topo-box {{
            background: linear-gradient(145deg, rgba(13, 27, 50, 0.82), rgba(7, 15, 30, 0.92));
            border: 1px solid rgba(56, 189, 248, 0.22);
            border-radius: 16px;
            padding: 14px 18px 10px;
            box-shadow: 0 8px 26px rgba(0,0,0,0.3);
        }}
        .topo-header {{
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 6px; flex-wrap: wrap; gap: 8px;
        }}
        .topo-title {{ font-size: 12px; font-weight: 700; color: #38BDF8; letter-spacing: 1px; }}
        .topo-badge {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px; font-weight: 700;
            color: {flow_color};
            background: {sub_glow};
            border: 1px solid {flow_color}66;
            padding: 4px 12px; border-radius: 999px;
        }}
        svg {{ width: 100%; height: 145px; display: block; }}
        .grid-line {{
            stroke: {flow_color};
            stroke-width: 4;
            stroke-opacity: 0.35;
        }}
        .energy-pulse {{
            stroke: #38BDF8;
            stroke-width: 5;
            stroke-linecap: round;
            stroke-dasharray: 18 42;
            opacity: {pulse_opacity};
            animation: flowMove {pulse_speed} linear infinite;
            filter: drop-shadow(0 0 6px #38BDF8);
        }}
        @keyframes flowMove {{
            from {{ stroke-dashoffset: 120; }}
            to {{ stroke-dashoffset: 0; }}
        }}
        .node-circle {{
            fill: #0B172E;
            stroke: {flow_color};
            stroke-width: 3.5;
            filter: drop-shadow(0 0 8px {sub_glow});
        }}
        .node-label {{
            fill: #E2E8F0;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.5px;
        }}
        .node-sub {{
            fill: #94A3B8;
            font-size: 9.5px;
        }}
    </style>
    </head>
    <body>
      <div class="topo-box">
        <div class="topo-header">
            <div class="topo-title">⚡ LIVE SMART GRID POWER FLOW &amp; BREAKER DIGITAL TWIN</div>
            <div class="topo-badge">● {status_text}</div>
        </div>
        <svg viewBox="0 0 920 145">
          <!-- Transmission Lines -->
          <line class="grid-line" x1="100" y1="60" x2="290" y2="60"/>
          <line class="energy-pulse" x1="100" y1="60" x2="290" y2="60"/>

          <line class="grid-line" x1="290" y1="60" x2="460" y2="60"/>
          <line class="energy-pulse" x1="290" y1="60" x2="460" y2="60"/>

          <!-- Circuit Breaker Gap between AI Substation (460) and Distribution (650) -->
          <line class="grid-line" x1="460" y1="60" x2="530" y2="60"/>
          <line x1="530" y1="60" x2="585" y2="60" stroke="{flow_color}" stroke-width="5"
                stroke-linecap="round" transform="rotate({breaker_angle} 530 60)"/>
          <text x="557" y="34" text-anchor="middle" fill="{flow_color}" font-size="10" font-weight="700">
            {"BREAKER OPEN" if abnormal else "BREAKER CLOSED"}
          </text>
          <line class="grid-line" x1="585" y1="60" x2="660" y2="60"/>
          <line class="energy-pulse" x1="585" y1="60" x2="660" y2="60"/>

          <line class="grid-line" x1="660" y1="60" x2="830" y2="60"/>
          <line class="energy-pulse" x1="660" y1="60" x2="830" y2="60"/>

          <!-- Nodes -->
          <g transform="translate(100,60)">
            <circle class="node-circle" r="24"/>
            <text y="5" text-anchor="middle" font-size="16">🏭</text>
            <text y="44" text-anchor="middle" class="node-label">POWER PLANT</text>
            <text y="58" text-anchor="middle" class="node-sub">11 kV Gen</text>
          </g>

          <g transform="translate(290,60)">
            <circle class="node-circle" r="24"/>
            <text y="5" text-anchor="middle" font-size="16">🗼</text>
            <text y="44" text-anchor="middle" class="node-label">TRANSMISSION</text>
            <text y="58" text-anchor="middle" class="node-sub">HV Bus</text>
          </g>

          <g transform="translate(460,60)">
            <circle class="node-circle" r="26"/>
            <text y="5" text-anchor="middle" font-size="17">🤖</text>
            <text y="44" text-anchor="middle" class="node-label">AI SUBSTATION</text>
            <text y="58" text-anchor="middle" class="node-sub">Dual-AI Guard</text>
          </g>

          <g transform="translate(660,60)">
            <circle class="node-circle" r="24"/>
            <text y="5" text-anchor="middle" font-size="16">🔌</text>
            <text y="44" text-anchor="middle" class="node-label">DISTRIBUTION</text>
            <text y="58" text-anchor="middle" class="node-sub">Feeder Line</text>
          </g>

          <g transform="translate(830,60)">
            <circle class="node-circle" r="24"/>
            <text y="5" text-anchor="middle" font-size="16">🏙️</text>
            <text y="44" text-anchor="middle" class="node-label">CONSUMERS</text>
            <text y="58" text-anchor="middle" class="node-sub">Smart Load</text>
          </g>
        </svg>
      </div>
    </body>
    </html>
    """
    components.html(html_topo, height=198, scrolling=False)


# =====================================================
# SMOOTH-MOTION ANIMATED METER GAUGE (PREV -> CURR)
# =====================================================

def render_gauge(title, value, prev_value, maximum, unit, safe_hint, minimum=0):
    """Animated SVG meter whose needle smoothly glides from prev_value to current value."""

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
        status, colour, bg_pill = "CRITICAL", "#F43F5E", "rgba(244, 63, 94, 0.16)"
    elif value < warning_low or value >= warning_high:
        status, colour, bg_pill = "WARNING", "#F59E0B", "rgba(245, 158, 11, 0.16)"
    else:
        status, colour, bg_pill = "NORMAL", "#10B981", "rgba(16, 185, 129, 0.16)"

    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@600;700&family=JetBrains+Mono:wght@700&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; }
        body {
            margin: 0; padding: 0;
            background: transparent;
            color: #F8FAFC;
            font-family: 'Inter', sans-serif;
        }
        .card {
            background: linear-gradient(160deg, rgba(16, 33, 60, 0.82), rgba(8, 17, 34, 0.92));
            border: 1px solid rgba(56, 189, 248, 0.22);
            border-radius: 16px;
            padding: 12px 10px 10px;
            text-align: center;
            min-height: 234px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.28);
        }
        .heading {
            font-size: 12px; font-weight: 700;
            color: #E2E8F0; margin: 2px 0 0;
            letter-spacing: 0.9px;
            text-transform: uppercase;
        }
        .hint {
            font-size: 10px; color: #64748B;
            margin-top: 2px; font-weight: 600;
        }
        svg { width: 100%; max-width: 255px; display: block; margin: 0 auto; }
        .track { fill: none; stroke: rgba(148, 163, 184, 0.16); stroke-width: 13; stroke-linecap: round; }
        .arc {
            fill: none; stroke: __COLOUR__; stroke-width: 13;
            stroke-linecap: round; stroke-dasharray: 377;
            stroke-dashoffset: __START_OFFSET__;
            filter: drop-shadow(0 0 8px __COLOUR__);
            transition: stroke-dashoffset 1.2s cubic-bezier(0.22, 1, 0.36, 1);
        }
        .needle {
            stroke: #F8FAFC; stroke-width: 3.5; stroke-linecap: round;
            transform-origin: 150px 150px;
            transform: rotate(__START_ANGLE__deg);
            transition: transform 1.2s cubic-bezier(0.22, 1, 0.36, 1);
        }
        .reading { font-family: 'JetBrains Mono', monospace; font-size: 23px; fill: #FFFFFF; font-weight: 700; }
        .small { fill: #64748B; font-size: 10px; font-weight: 600; }
        .status {
            display: inline-block; margin-top: 2px; padding: 4px 13px;
            border-radius: 999px; color: __COLOUR__;
            border: 1px solid __COLOUR__55;
            background: __STATUS_BG__; font-size: 10.5px; font-weight: 700;
            letter-spacing: 0.8px;
        }
    </style>
    </head>
    <body>
      <div class="card">
        <div class="heading">__TITLE__</div>
        <div class="hint">Nominal: __SAFE_HINT__</div>
        <svg viewBox="0 0 300 186" role="img" aria-label="__TITLE__ gauge">
          <path class="track" d="M 30 150 A 120 120 0 0 1 270 150"/>
          <path class="arc" id="arc" d="M 30 150 A 120 120 0 0 1 270 150"/>
          <line class="needle" id="needle" x1="150" y1="150" x2="150" y2="54"/>
          <circle cx="150" cy="150" r="7" fill="#38BDF8"/>
          <text x="150" y="180" text-anchor="middle" class="reading">__VALUE__</text>
          <text x="26" y="168" class="small">MIN</text>
          <text x="252" y="168" class="small">MAX</text>
        </svg>
        <div class="status">● __STATUS__</div>
      </div>
      <script>
        const targetAngle = -90 + (__RATIO__ * 180);
        const targetOffset = 377 * (1 - __RATIO__);
        setTimeout(() => {
          document.getElementById("needle").style.transform = "rotate(" + targetAngle + "deg)";
          document.getElementById("arc").style.strokeDashoffset = targetOffset;
        }, 60);
      </script>
    </body>
    </html>
    """

    start_angle = -90 + (prev_ratio * 180)
    start_offset = 377 * (1 - prev_ratio)

    replacements = {
        "__TITLE__": title,
        "__SAFE_HINT__": safe_hint,
        "__VALUE__": f"{value:.2f} {unit}",
        "__RATIO__": json.dumps(ratio),
        "__START_ANGLE__": json.dumps(start_angle),
        "__START_OFFSET__": json.dumps(start_offset),
        "__COLOUR__": colour,
        "__STATUS__": status,
        "__STATUS_BG__": bg_pill,
    }
    for key, replacement in replacements.items():
        html_code = html_code.replace(key, replacement)

    components.html(html_code, height=248, scrolling=False)


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
# SIDEBAR CONTROLS
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
if electrical_model is not None:
    st.sidebar.success("Electrical AI: ACTIVE")
else:
    st.sidebar.warning("Electrical AI: NOT LOADED")

if network_model is not None:
    st.sidebar.success("Network Security AI: ACTIVE")
else:
    st.sidebar.warning("Network Security AI: NOT LOADED")

st.sidebar.info(
    "Academic Prototype • All electrical values & breaker trips are simulated."
)

if st.sidebar.button("🔄 RESET GRID"):
    st.session_
