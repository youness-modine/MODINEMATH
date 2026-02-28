import streamlit as st
import requests
import json
import fitz
from fpdf import FPDF

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MODINEMATH COSMOS", page_icon="ζ", layout="wide")

# --- 2. سحر الأنيميشن المتقدم (Nebula Colors Edition) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #050505 !important;
    }

    .zeta-header {
        text-align: center;
        font-size: 75px;
        font-weight: 900;
        background: linear-gradient(90deg, #00d2ff, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 20px rgba(0, 210, 255, 0.4));
        margin-top: 30px;
    }

    /* أنيميشن الألوان المتغيرة (Color Shift) */
    @keyframes colorChange {
        0% { color: #00d2ff; text-shadow: 0 0 10px #00d2ff; }
        50% { color: #9b72cb; text-shadow: 0 0 20px #9b72cb; }
        100% { color: #00d2ff; text-shadow: 0 0 10px #00d2ff; }
    }

    @keyframes float {
        0% { 
            transform: translateY(110vh) rotate(0deg) scale(1); 
            opacity: 0; 
        }
        20% { opacity: 0.4; }
        80% { opacity: 0.4; }
        100% { 
            transform: translateY(-20vh) rotate(720deg) scale(1.2); 
            opacity: 0; 
        }
    }

    .particle {
        position: fixed;
        top: 0;
        font-family: 'serif';
        font-weight: bold;
        font-size: 32px; 
        user-select: none;
        pointer-events: none;
        z-index: 0;
        /* تفعيل أنيميشن تغيير الألوان */
        animation: float 15s infinite linear, colorChange 8s infinite ease-in-out;
    }

    div.stButton > button {
        background: transparent !important;
        color: #00d2ff !important;
        border: 2px solid #00d2ff !important;
        border-radius: 50px !important;
        padding: 10px 40px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 10px rgba(0, 210, 255, 0.2) !important;
    }

    div.stButton > button:hover {
        background: #00d2ff !important;
        color: #000 !important;
        box-shadow: 0 0 40px #00d2ff !important;
        transform: scale(1.05) !important;
    }
    </style>

    <div class="particle" style="left:5%; animation-duration: 14s, 7s;">β</div>
    <div class="particle" style="left:18%; animation-duration: 16s, 9s; animation-delay: 3s, 0s;">Γ</div>
    <div class="particle" style="left:35%; animation-duration: 13s, 6s; animation-delay: 1s, 0s;">∇</div>
    <div class="particle" style="left:55%; animation-duration: 19s, 10s; animation-delay: 6s, 0s;">[M]</div>
    <div class="particle" style="left:75%; animation-duration: 15s, 8s; animation-delay: 2s, 0s;">Π</div>
    
    <div class="particle" style="left:12%; animation-duration: 22s, 12s; font-size: 40px; opacity: 0.2;">○</div>
    <div class="particle" style="left:40%; animation-duration: 25s, 15s; font-size: 35px; opacity: 0.2; animation-delay: 4s, 0s;">△</div>
    <div class="particle" style="left:60%; animation-duration: 20s, 11s; font-size: 30px; opacity: 0.2; animation-delay: 7s, 0s;">□</div>
    <div class="particle" style="left:80%; animation-duration: 24s, 14s; font-size: 45px; opacity: 0.2; animation-delay: 5s, 0s;">▭</div>

    <div class="particle" style="left:22%; animation-duration: 12s, 5s;">∫</div>
    <div class="particle" style="left:50%; animation-duration: 18s, 10s; animation-delay: 5s, 0s;">∞</div>
    <div class="particle" style="left:10%; animation-duration: 12s, 6s;">ζ</div>
    <div class="particle" style="left:65%; animation-duration: 14s, 7s; animation-delay: 1s, 0s;">Σ</div>
    <div class="particle" style="left:85%; animation-duration: 16s, 8s; animation-delay: 4s, 0s;">π</div>
    <div class="particle" style="left:15%; animation-duration: 20s, 12s; animation-delay: 8s, 0s;">√</div>
    """, unsafe_allow_html=True)

# --- 3. محرك Groq الذكي ---
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

def generate_cosmos_ans(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "system", "content": "You are MODINEMATH, a cosmic math AI. Use LaTeX."},
                     {"role": "user", "content": prompt}],
        "stream": True
    }
    response = requests.post(url, headers=headers, json=payload, stream=True)
    for line in response.iter_lines():
        if line:
            decoded = line.decode('utf-8').replace('data: ', '')
            if decoded == '[DONE]': break
            try:
                chunk = json.loads(decoded)
                yield chunk['choices'][0]['delta'].get('content', '')
            except: continue

# --- 4. واجهة المستخدم ---
st.markdown('<div class="zeta-header">ζ MODINEMATH</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#8892b0;'>PROBING THE LIMITS OF MATHEMATICAL INTELLIGENCE</p>", unsafe_allow_html=True)

user_input = st.text_area("", placeholder="Ask the Cosmic Encyclopedia...", height=120, label_visibility="collapsed")

col1, col2, col3 = st.columns([1, 0.6, 1])
with col2:
    if st.button("IGNITE SOLVER ✨"):
        if user_input:
            full_ans = ""
            ans_container = st.empty()
            for chunk in generate_cosmos_ans(user_input):
                full_ans += chunk
                ans_container.markdown(f'<div style="color:#00d2ff;">{full_ans}▌</div>', unsafe_allow_html=True)
            ans_container.markdown(full_ans)

st.markdown("<br><br><p style='text-align:center; color:rgba(255,255,255,0.1);'>V12.3 | Developed by Youness Modine | UIT</p>", unsafe_allow_html=True)
