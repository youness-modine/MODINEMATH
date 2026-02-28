import streamlit as st
import requests
import json
import fitz
from fpdf import FPDF

# --- 1. إعدادات الصفحة والهوية ---
st.set_page_config(page_title="MODINEMATH COSMOS", page_icon="ζ", layout="wide")

# --- 2. سحر الـ CSS و الأنيميشن (The Dark Magic) ---
st.markdown("""
    <style>
    /* خلفية كونية متحركة */
    .stApp {
        background: #050505;
        overflow: hidden;
    }

    /* تأثير النجوم الرياضية (Mathematical Stars) */
    @keyframes move-symbols {
        from { transform: translateY(0px) rotate(0deg); opacity: 0.2; }
        to { transform: translateY(-1000px) rotate(360deg); opacity: 0; }
    }

    .math-symbol {
        position: fixed;
        color: rgba(0, 210, 255, 0.3);
        font-family: 'Times New Roman';
        z-index: -1;
        pointer-events: none;
        animation: move-symbols 15s linear infinite;
    }

    /* العنوان المتوهج (Neon Zeta) */
    .zeta-header {
        text-align: center;
        font-size: 80px;
        font-weight: bold;
        background: linear-gradient(90deg, #00d2ff, #92fe9d, #00d2ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 15px rgba(0, 210, 255, 0.5));
        margin-bottom: 0px;
    }

    /* أزرار تفاعلية بالضوء (Animated Buttons) */
    div.stButton > button {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #00d2ff !important;
        border: 1px solid #00d2ff !important;
        border-radius: 30px !important;
        padding: 15px 30px !important;
        font-size: 18px !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 0 5px rgba(0, 210, 255, 0.2) !important;
    }

    div.stButton > button:hover {
        background: #00d2ff !important;
        color: #000 !important;
        box-shadow: 0 0 30px #00d2ff, 0 0 60px rgba(0, 210, 255, 0.4) !important;
        transform: scale(1.05) translateY(-5px) !important;
    }

    /* صندوق الإدخال الزجاجي (Glassmorphism) */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        color: #fff !important;
        backdrop-filter: blur(10px) !important;
    }

    .stTextArea textarea:focus {
        border-color: #00d2ff !important;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.3) !important;
    }
    </style>
    
    <div class="math-symbol" style="left: 10%; bottom: -100px; font-size: 30px;">∫</div>
    <div class="math-symbol" style="left: 30%; bottom: -200px; font-size: 20px; animation-delay: 2s;">∑</div>
    <div class="math-symbol" style="left: 50%; bottom: -150px; font-size: 40px; animation-delay: 5s;">π</div>
    <div class="math-symbol" style="left: 70%; bottom: -300px; font-size: 25px; animation-delay: 7s;">√</div>
    <div class="math-symbol" style="left: 90%; bottom: -100px; font-size: 35px; animation-delay: 1s;">∞</div>
    """, unsafe_allow_html=True)

# --- 3. المحرك الذكي (The Brain) ---
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

def generate_cosmos_response(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are MODINEMATH, an elite cosmic mathematician. Solve rigorously. Use LaTeX. Support all languages specified like [Chinese]."},
            {"role": "user", "content": prompt}
        ],
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
st.markdown("<p style='text-align:center; color:#8892b0; font-family: monospace;'>PROBING THE LIMITS OF MATHEMATICAL INTELLIGENCE</p>", unsafe_allow_html=True)

# مساحة الدردشة
user_input = st.text_area("", placeholder="Ask the Cosmic Encyclopedia...", height=120)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("IGNITE SOLVER ✨"):
        if user_input:
            full_response = ""
            st.markdown("### 🎓 Cosmic Derivation:")
            ans_area = st.empty()
            for chunk in generate_cosmos_response(user_input):
                full_response += chunk
                ans_area.markdown(f'<div style="color:#00d2ff; text-shadow: 0 0 10px rgba(0,210,255,0.2);">{full_response}▌</div>', unsafe_allow_html=True)
            ans_area.markdown(f'<div style="color:#e0e0e0;">{full_response}</div>', unsafe_allow_html=True)

# تذييل الصفحة
st.markdown("<br><br><p style='text-align:center; color:rgba(255,255,255,0.1);'>V12.0 | Developed by Youness Modine | UIT</p>", unsafe_allow_html=True)
