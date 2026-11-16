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
# LOCKED DARK COMMAND CENTER CSS
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

html, body, .stApp, [data-testid="stAppViewContainer"] {
    background-color: #060E1C !important;
    color: #F8FAFC !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

header[data-testid="stHeader"] {
    background-color: #060E1C !important;
}

section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div {
    background-color: #091528 !important;
    border-right: 1px solid #1E3A5F !important;
}

section[data-testid="stSidebar"] * {
    color: #F8FAFC !important;
}

/* Dropdown & Number Inputs Locked Dark */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
input {
    background-color: #112645 !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    border: 1px solid #38BDF8 !important;
    border-radius: 10px !important;
}
div[data-baseweb="select"] span,
div[data-baseweb="select"] div {
    background-color: transparent !important;
    color: #FFFFFF !important;
}
ul[role="listbox"], li[role="option"] {
    background-color: #112645 !important;
    color: #FFFFFF !important;
}
li[role="option"]:hover {
    background-color: #1D4ED8 !important;
}

/* Hero Banner */
.hero-banner {
    background: linear-gradient(135deg, #0F2547 0%, #09162B 100%);
    border: 1px solid #2563EB;
    border-radius: 16px;
    padding: 18px 24px;
    margin-bottom: 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
}
.hero-title {
    font-size: 26px;
    font-weight: 800;
    color: #38BDF8;
    margin: 0;
}
.hero-sub {
    color: #CBD5E1;
    font-size: 13px;
    margin: 4px 0 0 0;
}
.live-pill {
    background: rgba(16, 185, 129, 0.16);
    border: 1px solid #10B981;
    color: #34D399;
    padding: 7px 15px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
}

/* 3-Step Concept Strip */
.concept-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 12px;
    margin-bottom: 14px;
}
.concept-card {
    background: #0D1E3B;
    border: 1px solid #1E3A5F;
    border-radius: 12px;
    padding: 12px 15px;
    display: flex;
    align-items: center;
    gap: 12px;
}
.concept-icon {
    font-size: 20px;
    background: #132B52;
    border: 1px solid #38BDF8;
    border-radius: 10px;
    width: 40px;
    height: 40px;
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
}
.concept-desc {
    font-size: 12px;
    color: #E2E8F0;
    margin-top: 2px;
}

.section-label {
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #38BDF8;
    margin: 16px 0 10px 0;
}

.status-banner {
    padding: 13px 18px;
    border-radius: 12px;
    font-weight: 700;
    font-size: 14px;
    margin-bottom: 12px;
    border: 1px solid;
}
.status-ok { background: #064E3B; border-color: #10B981; color: #ECFDF5; }
.status-warn { background: #78350F; border-color: #F59E0B; color: #FFFBEB; }
.status-crit { background: #881337; border-color: #F43F5E; color: #FFF1F2; }

[data-testid="stMetric"] {
    background-color: #0D1E3B !important;
    border: 1px solid #1E3A5F !important;
    border-radius: 12px !important;
    padding: 12px 14px !important;
}
[data-testid="stMetricLabel"] { color: #94A3B8 !important; font-size: 11px !important; font-weight: 700 !important; }
[data-testid="stMetricValue"] { color: #FFFFFF !important; font-family: 'JetBrains Mono', monospace !important; font-size: 20px !important; }

.stButton > button, .stDownloadButton > button {
    background: linear-gradient(135deg, #0284C7, #2563EB) !important;
    color: #FFFFFF !important;
    border: 1px solid #38BDF8 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}
section[data-testid="stSidebar"] .stButton > button { width: 100% !important; }
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
# ELECTRICAL AI PREDICTION & SIMULATION
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
# ZERO-BLINK 60FPS SMOOTH MOTION TOPOLOGY + 6 METERS
# =====================================================

def render_realtime_motion_twin(latest, scenario, running):
    """Renders the power flow topology + 6 smooth-motion analog/digital gauges in a single zero-flicker HTML/JS canvas."""
    abnormal_js = "true" if latest["abnormal"] else "false"
    running_js = "true" if running else "false"

    html_twin = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
      * {{ box-sizing: border-box; margin: 0; padding: 0; }}
      body {{
        background: #060E1C;
        color: #F8FAFC;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      }}
      .topo-box {{
        background: #0D1E3B;
        border: 1px solid #1E3A5F;
        border-radius: 16px;
        padding: 14px 18px 10px;
        margin-bottom: 14px;
      }}
      .topo-header {{
        display: flex; justify-content: space-between; align-items: center;
        margin-bottom: 6px; flex-wrap: wrap; gap: 8px;
      }}
      .topo-title {{ font-size: 12px; font-weight: 700; color: #38BDF8; letter-spacing: 1px; }}
      .topo-badge {{
        font-size: 11px; font-weight: 700; padding: 4px 12px; border-radius: 999px;
      }}
      .grid-line {{ stroke-width: 4; stroke-opacity: 0.35; transition: stroke 0.4s; }}
      .energy-pulse {{
        stroke: #38BDF8; stroke-width: 5; stroke-linecap: round;
        stroke-dasharray: 18 42;
        animation: flowMove 1.4s linear infinite;
      }}
      @keyframes flowMove {{
        from {{ stroke-dashoffset: 120; }}
        to {{ stroke-dashoffset: 0; }}
      }}
      .node-circle {{ fill: #091528; stroke-width: 3.5; transition: stroke 0.4s; }}
      .node-label {{ fill: #FFFFFF; font-size: 11px; font-weight: 700; }}
      .node-sub {{ fill: #94A3B8; font-size: 9.5px; }}

      .section-title {{
        font-size: 12px; font-weight: 700; color: #38BDF8;
        letter-spacing: 1px; text-transform: uppercase; margin: 10px 0;
      }}
      .meters-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 14px;
      }}
      @media (max-width: 820px) {{
        .meters-grid {{ grid-template-columns: repeat(2, 1fr); }}
      }}
      @media (max-width: 520px) {{
        .meters-grid {{ grid-template-columns: 1fr; }}
      }}
      .meter-card {{
        background: #0D1E3B;
        border: 1px solid #1E3A5F;
        border-radius: 16px;
        padding: 12px 10px 10px;
        text-align: center;
      }}
      .m-title {{ font-size: 12px; font-weight: 700; color: #FFFFFF; letter-spacing: 0.8px; }}
      .m-hint {{ font-size: 10px; color: #94A3B8; margin-top: 2px; }}
      .m-svg {{ width: 100%; max-width: 245px; display: block; margin: 0 auto; }}
      .m-track {{ fill: none; stroke: #1E3A5F; stroke-width: 13; stroke-linecap: round; }}
      .m-arc {{
        fill: none; stroke-width: 13; stroke-linecap: round; stroke-dasharray: 377;
        transition: stroke-dashoffset 0.9s cubic-bezier(0.22, 1, 0.36, 1), stroke 0.4s;
      }}
      .m-needle {{
        stroke: #FFFFFF; stroke-width: 3.5; stroke-linecap: round;
        transform-origin: 150px 150px;
        transition: transform 0.9s cubic-bezier(0.22, 1, 0.36, 1);
      }}
      .m-val {{ font-size: 21px; fill: #FFFFFF; font-weight: 700; font-family: monospace; }}
      .m-small {{ fill: #94A3B8; font-size: 10px; font-weight: 600; }}
      .m-pill {{
        display: inline-block; margin-top: 2px; padding: 4px 13px;
        border-radius: 999px; font-size: 10.5px; font-weight: 700;
        border: 1px solid; transition: all 0.4s;
      }}
    </style>
    </head>
    <body>
      <!-- LIVE POWER FLOW TOPOLOGY -->
      <div class="topo-box">
        <div class="topo-header">
          <div class="topo-title">⚡ LIVE SMART GRID POWER FLOW &amp; BREAKER DIGITAL TWIN</div>
          <div class="topo-badge" id="topoBadge">● ENERGIZED</div>
        </div>
        <svg viewBox="0 0 920 135" style="width:100%; height:135px; display:block;">
          <line class="grid-line" id="l1" x1="100" y1="55" x2="290" y2="55"/>
          <line class="energy-pulse" id="p1" x1="100" y1="55" x2="290" y2="55"/>
          <line class="grid-line" id="l2" x1="290" y1="55" x2="460" y2="55"/>
          <line class="energy-pulse" id="p2" x1="290" y1="55" x2="460" y2="55"/>
          <line class="grid-line" id="l3" x1="460" y1="55" x2="530" y2="55"/>
          <line id="breakerArm" x1="530" y1="55" x2="585" y2="55" stroke="#10B981" stroke-width="5"
                stroke-linecap="round" style="transition: transform 0.5s;"/>
          <text id="breakerText" x="557" y="30" text-anchor="middle" fill="#10B981" font-size="10" font-weight="700">BREAKER CLOSED</text>
          <line class="grid-line" id="l4" x1="585" y1="55" x2="660" y2="55"/>
          <line class="energy-pulse" id="p3" x1="585" y1="55" x2="660" y2="55"/>
          <line class="grid-line" id="l5" x1="660" y1="55" x2="830" y2="55"/>
          <line class="energy-pulse" id="p4" x1="660" y1="55" x2="830" y2="55"/>

          <g transform="translate(100,55)">
            <circle class="node-circle" id="n1" r="22"/><text y="5" text-anchor="middle" font-size="15">🏭</text>
            <text y="40" text-anchor="middle" class="node-label">POWER PLANT</text>
            <text y="54" text-anchor="middle" class="node-sub">11 kV Gen</text>
          </g>
          <g transform="translate(290,55)">
            <circle class="node-circle" id="n2" r="22"/><text y="5" text-anchor="middle" font-size="15">🗼</text>
            <text y="40" text-anchor="middle" class="node-label">TRANSMISSION</text>
            <text y="54" text-anchor="middle" class="node-sub">HV Bus</text>
          </g>
          <g transform="translate(460,55)">
            <circle class="node-circle" id="n3" r="24"/><text y="5" text-anchor="middle" font-size="16">🤖</text>
            <text y="40" text-anchor="middle" class="node-label">AI SUBSTATION</text>
            <text y="54" text-anchor="middle" class="node-sub">Dual-AI Guard</text>
          </g>
          <g transform="translate(660,55)">
            <circle class="node-circle" id="n4" r="22"/><text y="5" text-anchor="middle" font-size="15">🔌</text>
            <text y="40" text-anchor="middle" class="node-label">DISTRIBUTION</text>
            <text y="54" text-anchor="middle" class="node-sub">Feeder Line</text>
          </g>
          <g transform="translate(830,55)">
            <circle class="node-circle" id="n5" r="22"/><text y="5" text-anchor="middle" font-size="15">🏙️</text>
            <text y="40" text-anchor="middle" class="node-label">CONSUMERS</text>
            <text y="54" text-anchor="middle" class="node-sub">Smart Load</text>
          </g>
        </svg>
      </div>

      <div class="section-title">🎯 LIVE SMOOTH-MOTION INSTRUMENTATION METERS (REAL-TIME)</div>
      <div class="meters-grid" id="metersGrid"></div>

      <script>
        const scenario = {json.dumps(scenario)};
        const isRunning = {running_js};

        const meterConfigs = [
          {{ id: "volt", title: "VOLTAGE", unit: "kV", min: 8, max: 12, hint: "Safe: 10.5 – 11.5 kV", val: {latest["voltage_kv"]}, critLow: 10.0, warnLow: 10.5, warnHigh: 11.5, critHigh: 11.8 }},
          {{ id: "curr", title: "CURRENT", unit: "A", min: 0, max: 500, hint: "Safe: < 380 A", val: {latest["current_a"]}, critLow: -999, warnLow: -999, warnHigh: 380, critHigh: 430 }},
          {{ id: "freq", title: "FREQUENCY", unit: "Hz", min: 45, max: 55, hint: "Safe: 49.5 – 50.5 Hz", val: {latest["frequency_hz"]}, critLow: 49.5, warnLow: 49.7, warnHigh: 50.3, critHigh: 50.5 }},
          {{ id: "pow",  title: "POWER", unit: "MW", min: 0, max: 12, hint: "Safe: < 7.5 MW", val: {latest["power_mw"]}, critLow: -999, warnLow: -999, warnHigh: 7.5, critHigh: 8.5 }},
          {{ id: "load", title: "GRID LOAD", unit: "%", min: 0, max: 130, hint: "Safe: < 90 %", val: {latest["load_percent"]}, critLow: -999, warnLow: -999, warnHigh: 90, critHigh: 100 }},
          {{ id: "temp", title: "TRANSFORMER TEMP", unit: "°C", min: 0, max: 110, hint: "Safe: < 75 °C", val: {latest["transformer_temp_c"]}, critLow: -999, warnLow: -999, warnHigh: 75, critHigh: 85 }}
        ];

        const grid = document.getElementById("metersGrid");
        meterConfigs.forEach(m => {{
          grid.innerHTML += `
            <div class="meter-card">
              <div class="m-title">${{m.title}}</div>
              <div class="m-hint">${{m.hint}}</div>
              <svg class="m-svg" viewBox="0 0 300 184">
                <path class="m-track" d="M 30 150 A 120 120 0 0 1 270 150"/>
                <path class="m-arc" id="arc_${{m.id}}" d="M 30 150 A 120 120 0 0 1 270 150"/>
                <line class="m-needle" id="needle_${{m.id}}" x1="150" y1="150" x2="150" y2="54"/>
                <circle cx="150" cy="150" r="7" fill="#38BDF8"/>
                <text x="150" y="179" text-anchor="middle" class="m-val" id="val_${{m.id}}">0.00</text>
                <text x="26" y="168" class="m-small">MIN</text>
                <text x="252" y="168" class="m-small">MAX</text>
              </svg>
              <div class="m-pill" id="pill_${{m.id}}">● NORMAL</div>
            </div>
          `;
        }});

        function updateVisuals(vMap, isAbnormal) {{
          const flowColor = isAbnormal ? "#F43F5E" : "#10B981";
          ["l1","l2","l3","l4","l5"].forEach(id => document.getElementById(id).style.stroke = flowColor);
          ["n1","n2","n3","n4","n5"].forEach(id => document.getElementById(id).style.stroke = flowColor);
          ["p1","p2","p3","p4"].forEach(id => document.getElementById(id).style.opacity = isAbnormal ? "0" : "1");

          const arm = document.getElementById("breakerArm");
          arm.style.stroke = flowColor;
          arm.setAttribute("transform", isAbnormal ? "rotate(-38 530 55)" : "rotate(0 530 55)");
          const bTxt = document.getElementById("breakerText");
          bTxt.style.fill = flowColor;
          bTxt.textContent = isAbnormal ? "BREAKER OPEN" : "BREAKER CLOSED";

          const badge = document.getElementById("topoBadge");
          badge.style.color = flowColor;
          badge.style.borderColor = flowColor;
          badge.style.background = isAbnormal ? "rgba(244,63,94,0.18)" : "rgba(16,185,129,0.18)";
          badge.textContent = isAbnormal
            ? "● FAULT ISOLATED • BREAKER OPEN"
            : `● ENERGIZED • ${{vMap.pow.toFixed(2)}} MW FLOWING (${{vMap.load.toFixed(0)}}% LOAD)`;

          meterConfigs.forEach(m => {{
            const val = vMap[m.id];
            const ratio = Math.max(0, Math.min(1, (val - m.min) / (m.max - m.min)));
            const angle = -90 + ratio * 180;
            const offset = 377 * (1 - ratio);

            let status = "NORMAL", col = "#10B981", bg = "rgba(16,185,129,0.18)";
            if (val < m.critLow || val >= m.critHigh) {{
              status = "CRITICAL"; col = "#F43F5E"; bg = "rgba(244,63,94,0.18)";
            }} else if (val < m.warnLow || val >= m.warnHigh) {{
              status = "WARNING"; col = "#F59E0B"; bg = "rgba(245,158,11,0.18)";
            }}

            const arc = document.getElementById("arc_" + m.id);
            arc.style.stroke = col;
            arc.style.strokeDashoffset = offset;

            document.getElementById("needle_" + m.id).style.transform = `rotate(${{angle}}deg)`;
            document.getElementById("val_" + m.id).textContent = `${{val.toFixed(2)}} ${{m.unit}}`;

            const pill = document.getElementById("pill_" + m.id);
            pill.textContent = `● ${{status}}`;
            pill.style.color = col;
            pill.style.borderColor = col;
            pill.style.background = bg;
          }});
        }}

        function rand(min, max) {{ return Math.random() * (max - min) + min; }}

        function tickSimulation() {{
          let volt = rand(10.9, 11.1), curr = rand(260, 310), freq = rand(49.95, 50.05);
          let load = rand(65, 85), temp = rand(55, 68), abn = false;

          if (scenario === "OVERLOAD") {{
            curr = rand(430, 480); load = rand(115, 130); temp = rand(90, 105); abn = true;
          }} else if (scenario === "VOLTAGE DIP") {{
            volt = rand(8.5, 9.5); abn = true;
          }} else if (scenario === "FREQUENCY DEVIATION") {{
            freq = rand(47.5, 48.5); abn = true;
          }} else if (scenario === "TRANSFORMER OVERHEATING") {{
            curr = rand(290, 340); load = rand(78, 92); temp = rand(88, 102); abn = true;
          }} else if (scenario === "COMMUNICATION ANOMALY" || scenario === "SWITCHING ANOMALY") {{
            abn = true;
          }}

          const pow = (volt * curr * Math.sqrt(3)) / 1000;
          updateVisuals({{ volt, curr, freq, pow, load, temp }}, abn);
        }}

        // Initial render from Python AI model state
        updateVisuals({{
          volt: {latest["voltage_kv"]},
          curr: {latest["current_a"]},
          freq: {latest["frequency_hz"]},
          pow: {latest["power_mw"]},
          load: {latest["load_percent"]},
          temp: {latest["transformer_temp_c"]}
        }}, {abnormal_js});

        // Smooth continuous needle motion every 1.6s without page flicker!
        if (isRunning) {{
          setInterval(tickSimulation, 1600);
        }}
      </script>
    </body>
    </html>
    """
    components.html(html_twin, height=705, scrolling=False)


# =====================================================
# HEADER & 3-STEP CONCEPT CLARITY STRIP
# =====================================================

st.markdown("""
<div class="hero-banner">
    <div>
        <h1 class="hero-title">🛡️ GRIDSHIELD AI</h1>
        <p class="hero-sub">Real-Time Smart Grid Digital Twin • Dual-AI Physical &amp; Cybersecurity Protection</p>
    </div>
    <div class="live-pill">● LIVE DIGITAL TWIN ACTIVE</div>
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

elec_badge = "ACTIVE ✅" if electrical_model is not None else "OFFLINE ⚠️"
net_badge = "ACTIVE ✅" if network_model is not None else "OFFLINE ⚠️"

st.sidebar.markdown(f"""
<div style="background:#112645; border:1px solid #10B981; border-radius:10px; padding:10px 12px; margin-bottom:8px; color:#FFFFFF; font-size:13px; font-weight:600;">
    ⚡ Electrical AI: {elec_badge}
</div>
<div style="background:#112645; border:1px solid #10B981; border-radius:10px; padding:10px 12px; margin-bottom:10px; color:#FFFFFF; font-size:13px; font-weight:600;">
    🛡️ Network Security AI: {net_badge}
</div>
<div style="background:#0D1E3B; border:1px solid #38BDF8; border-radius:10px; padding:10px 12px; margin-bottom:12px; color:#CBD5E1; font-size:12px;">
    Academic Prototype • All electrical values &amp; breaker trips are simulated.
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("🔄 SAMPLE NEW READING"):
    st.rerun()

if st.sidebar.button("🗑️ RESET HISTORY"):
    st.session_state.history = []
    st.session_state.events = []
    st.session_state.total_analyses = 0
    st.session_state.normal_count = 0
    st.session_state.abnormal_count = 0
    st.session_state.last_network_status = "Normal"
    st.rerun()


# =====================================================
# GENERATE READING FOR SELECTED SCENARIO
# =====================================================

reading = generate_reading(st.session_state.scenario)
st.session_state.history.append(reading)
st.session_state.history = st.session_state.history[-30:]
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

# ZERO-BLINK REALTIME MOTION TOPOLOGY + 6 METERS
render_realtime_motion_twin(latest, st.session_state.scenario, st.session_state.running)

# ELECTRICAL AI DIAGNOSIS & PROTECTION
st.markdown('<div class="section-label">🤖 ELECTRICAL AI ANOMALY DETECTION &amp; AUTOMATED PROTECTION</div>', unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
m1.metric("AI Predicted Condition", latest["ai_condition"])
m2.metric("Prediction Confidence", f'{latest["ai_confidence"]:.1f} %')
m3.metric("Protection Relay", "TRIGGERED" if abnormal else "NORMAL")
m4.metric("Circuit Breaker", "OPEN (ISOLATED)" if abnormal else "CLOSED")

diag_class = "status-crit" if latest["ai_abnormal"] else "status-ok"
diag_icon = "⚠️" if latest["ai_abnormal"] else "✅"
st.markdown(f'<div class="status-banner {diag_class}">{diag_icon} Electrical AI Diagnosis: {latest["ai_explanation"]}</div>', unsafe_allow_html=True)

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
