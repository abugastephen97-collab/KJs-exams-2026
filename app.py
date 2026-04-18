"""
KJS Junior School Exam Management System
Streamlit App — Online Version
Compatible data structure with Excel workbook
"""

import streamlit as st
import pandas as pd
import json
import io
from datetime import datetime

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="KJS Exam System",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main-header {
    background: linear-gradient(135deg, #C0392B, #922B21);
    color: white; padding: 20px 30px; border-radius: 12px;
    margin-bottom: 20px; text-align: center;
}
.main-header h1 { margin: 0; font-size: 1.8rem; font-weight: 700; }
.main-header p { margin: 4px 0 0; opacity: 0.85; font-size: 0.9rem; }
.metric-card {
    background: #f8f9fa; border-left: 4px solid #C0392B;
    padding: 12px 16px; border-radius: 8px; margin: 4px 0;
}
.rubric-EE1{background:#D6EAF8;color:#1A5276;font-weight:700;padding:3px 10px;border-radius:6px;display:inline-block}
.rubric-EE2{background:#D6EAF8;color:#2E86C1;font-weight:700;padding:3px 10px;border-radius:6px;display:inline-block}
.rubric-ME1{background:#D5F5E3;color:#1E8449;font-weight:700;padding:3px 10px;border-radius:6px;display:inline-block}
.rubric-ME2{background:#D5F5E3;color:#239B56;font-weight:700;padding:3px 10px;border-radius:6px;display:inline-block}
.rubric-AE1{background:#FDEBD0;color:#E67E22;font-weight:700;padding:3px 10px;border-radius:6px;display:inline-block}
.rubric-AE2{background:#FDEBD0;color:#CA6F1E;font-weight:700;padding:3px 10px;border-radius:6px;display:inline-block}
.rubric-BE1{background:#FADBD8;color:#E74C3C;font-weight:700;padding:3px 10px;border-radius:6px;display:inline-block}
.rubric-BE2{background:#FADBD8;color:#C0392B;font-weight:700;padding:3px 10px;border-radius:6px;display:inline-block}
.stButton>button {
    border-radius: 8px; font-weight: 600; transition: all 0.2s;
}
div[data-testid="stExpander"] { border: 1px solid #e0e0e0; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ─── DEFAULT DATA ─────────────────────────────────────────────────────────────
DEFAULT_RUBRICS = [
    {"code":"EE1","desc":"Exceeding Expectation (High)","low":90,"high":100,"pts":8},
    {"code":"EE2","desc":"Exceeding Expectation",       "low":80,"high":89, "pts":7},
    {"code":"ME1","desc":"Meeting Expectation (High)",  "low":70,"high":79, "pts":6},
    {"code":"ME2","desc":"Meeting Expectation",         "low":60,"high":69, "pts":5},
    {"code":"AE1","desc":"Approaching Expectation (High)","low":50,"high":59,"pts":4},
    {"code":"AE2","desc":"Approaching Expectation",     "low":40,"high":49, "pts":3},
    {"code":"BE1","desc":"Below Expectation (High)",    "low":20,"high":39, "pts":2},
    {"code":"BE2","desc":"Below Expectation",           "low":0, "high":19, "pts":1},
]
DEFAULT_SUBJECTS = [
    {"code":"901","name":"English"},{"code":"902","name":"Kiswahili"},
    {"code":"903","name":"Mathematics"},{"code":"907","name":"Social Studies"},
    {"code":"908","name":"CRE"},{"code":"912","name":"Pre-Technical Studies"},
    {"code":"906","name":"Agriculture"},{"code":"905","name":"Integrated Science"},
    {"code":"911","name":"Creative Arts & Sports"},
]
DEFAULT_REMARKS_T = {
    "EE1":"Outstanding performance! You have exceeded all expectations. Keep it up.",
    "EE2":"Excellent work! You consistently exceed expectations.",
    "ME1":"Very good performance. You are mee
