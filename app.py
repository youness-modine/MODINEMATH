import streamlit as st
import requests
import json
import fitz
from fpdf import FPDF

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MODINEMATH COSMOS", page_icon="ζ", layout="wide")

# --- 2. سحر الأنيميشن المتقدم (HTML + CSS Injection) ---
st.markdown("""
    <style>
    /* خلفية Gemini/Grok العميقة */
    .stApp {
        background-color: #050505 !important;
    }

    /* تأثير التوهج للعنوان */
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

    /* أنيميشن الرموز والأشكال الإبداعية */
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
        color: #00d2ff;
        font-family: 'serif';
        font-weight: bold;
        font-size: 32px; 
        user-select: none;
        pointer-events: none;
        z-index: 0;
        text-shadow: 0 0 10px rgba(0, 210, 255, 0.5);
    }

    /* مظهر الأزرار التفاعلي */
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

    <div class="particle" style="left:5%; animation: float 14s infinite linear;">β</div>
    <div class="particle" style="left:18%; animation: float 16s infinite linear; animation-delay: 3s;">Γ</div>
    <div class="particle" style="left:35%; animation: float 13s infinite linear; animation-delay: 1s;">∇</div>
    <div class="particle" style="left:55%; animation: float 19s infinite linear; animation-delay: 6s;">[M]</div>
    <div class="particle" style="left:75%; animation: float 15s infinite linear; animation-delay: 2s;">Π</div>
    
    <div class="particle" style="left:12%; animation: float 22s infinite linear; font-size: 40px; opacity: 0.2;">○</div>
    <div class="particle" style="left:40%; animation: float 25s infinite linear; font-size: 35px; opacity: 0.2; animation-delay: 4s;">△</div>
    <div class="particle" style="left:60%; animation: float 20s infinite linear; font-size: 30px; opacity: 0.2; animation-delay: 7s;">□</div>
    <div class="particle" style="left:80%; animation: float 24s infinite linear; font-size: 45px; opacity: 0.2; animation-delay: 5s;">▭</div>

    <div class="particle" style="left:22%; animation: float 12s infinite linear;">∫</div>
    <div class="particle" style="left:50%; animation: float 18s infinite linear; animation-delay: 5s;">∞</div>
    <div class="particle" style="left:10%; animation: float 12s infinite linear;">ζ</div>
    <div class="particle" style="left:65%; animation: float 14s infinite linear; animation-delay: 1s;">Σ</div>
    <div class="particle" style="left:85%; animation: float 16s infinite linear; animation-delay: 4s;">π</div>
    <div class="particle" style="left:15%; animation: float 20s infinite linear; animation-delay: 8s;">√</div>
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

st.markdown("<br><br><p style='text-align:center; color:rgba(255,255,255,0.1);'>V12.2 | Developed by Youness Modine | UIT</p>", unsafe_allow_html=True)
