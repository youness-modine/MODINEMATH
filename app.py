import streamlit as st
import requests
import json
import fitz
from fpdf import FPDF

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MODINEMATH COSMOS", page_icon="ζ", layout="wide")

# --- 2. سحر الأنيميشن (Sky & Cloud Edition) ---
st.markdown("""
    <style>
    .stApp { background-color: #050505 !important; }
    .zeta-header {
        text-align: center;
        font-size: 75px; font-weight: 900;
        background: linear-gradient(90deg, #00bcff, #ffffff, #00bcff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 15px rgba(0, 188, 255, 0.6));
        margin-top: 30px;
    }
    @keyframes colorChange {
        0% { color: #00bcff; text-shadow: 0 0 10px #00bcff; }
        50% { color: #ffffff; text-shadow: 0 0 20px #ffffff; }
        100% { color: #00bcff; text-shadow: 0 0 10px #00bcff; }
    }
    @keyframes float {
        0% { transform: translateY(110vh) rotate(0deg) scale(1); opacity: 0; }
        20% { opacity: 0.5; }
        80% { opacity: 0.5; }
        100% { transform: translateY(-20vh) rotate(720deg) scale(1.2); opacity: 0; }
    }
    .particle {
        position: fixed; top: 0; font-family: 'serif'; font-weight: bold;
        font-size: 32px; user-select: none; pointer-events: none; z-index: 0;
        animation: float 15s infinite linear, colorChange 6s infinite ease-in-out;
    }
    div.stButton > button {
        background: transparent !important; color: #00bcff !important;
        border: 2px solid #00bcff !important; border-radius: 50px !important;
        padding: 10px 40px !important; font-weight: bold !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 10px rgba(0, 188, 255, 0.3) !important;
    }
    div.stButton > button:hover {
        background: #00bcff !important; color: #000 !important;
        box-shadow: 0 0 40px #00bcff !important; transform: scale(1.05) !important;
    }
    
    /* تعديل عرض حاوية الجواب ليكون عريضاً جداً */
    .response-container {
        color: #ffffff; 
        background: rgba(255,255,255,0.05); 
        padding: 30px; 
        border-radius: 15px;
        width: 100%;
        margin-top: 20px;
        font-size: 18px;
        line-height: 1.6;
    }
    </style>

    <div class="particle" style="left:5%; animation-duration: 14s, 5s;">β</div>
    <div class="particle" style="left:18%; animation-duration: 16s, 7s; animation-delay: 3s, 0s;">Γ</div>
    <div class="particle" style="left:35%; animation-duration: 13s, 4s; animation-delay: 1s, 0s;">∇</div>
    <div class="particle" style="left:55%; animation-duration: 19s, 8s; animation-delay: 6s, 0s;">[M]</div>
    <div class="particle" style="left:75%; animation-duration: 15s, 6s; animation-delay: 2s, 0s;">Π</div>
    <div class="particle" style="left:12%; animation-duration: 22s, 10s; font-size: 40px; opacity: 0.2;">○</div>
    <div class="particle" style="left:40%; animation-duration: 25s, 12s; font-size: 35px; opacity: 0.2; animation-delay: 4s, 0s;">△</div>
    <div class="particle" style="left:60%; animation-duration: 20s, 9s; font-size: 30px; opacity: 0.2; animation-delay: 7s, 0s;">□</div>
    <div class="particle" style="left:80%; animation-duration: 24s, 11s; font-size: 45px; opacity: 0.2; animation-delay: 5s, 0s;">▭</div>
    <div class="particle" style="left:22%; animation-duration: 12s, 4s;">∫</div>
    <div class="particle" style="left:50%; animation-duration: 18s, 8s; animation-delay: 5s, 0s;">∞</div>
    <div class="particle" style="left:10%; animation-duration: 12s, 5s;">ζ</div>
    <div class="particle" style="left:65%; animation-duration: 14s, 6s; animation-delay: 1s, 0s;">Σ</div>
    <div class="particle" style="left:85%; animation-duration: 16s, 7s; animation-delay: 4s, 0s;">π</div>
    <div class="particle" style="left:15%; animation-duration: 20s, 10s; animation-delay: 8s, 0s;">√</div>
    """, unsafe_allow_html=True)

# --- 3. محرك Groq (Llama 3.3) ---
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

def generate_cosmos_ans(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": "You are MODINEMATH, a math expert. Use LaTeX."},
                     {"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Connection Error: {str(e)}"

# --- 4. واجهة المستخدم ---
st.markdown('<div class="zeta-header">ζ MODINEMATH</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#ffffff; opacity:0.7;'>PROBING THE LIMITS OF MATHEMATICAL INTELLIGENCE</p>", unsafe_allow_html=True)

# خانة السؤال العريضة
user_input = st.text_area("", placeholder="Ask the Cosmic Encyclopedia...", height=150, label_visibility="collapsed")

# البوطونة في الوسط
col_btn1, col_btn2, col_btn3 = st.columns([1, 0.4, 1])
with col_btn2:
    submit = st.button("IGNITE SOLVER ✨")

# عرض الجواب بعرض الشاشة كامل
if submit and user_input:
    with st.spinner("Analyzing the Cosmos..."):
        ans = generate_cosmos_ans(user_input)
        st.markdown(f'<div class="response-container">{ans}</div>', unsafe_allow_html=True)

st.markdown("<br><br><p style='text-align:center; color:rgba(255,255,255,0.2);'>V12.7 | Wide Display Edition | Youness Modine</p>", unsafe_allow_html=True)
