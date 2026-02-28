import streamlit as st
import requests
import json
import google.generativeai as genai
from fpdf import FPDF
import io

# --- 1. إعدادات الصفحة والهوية ---
st.set_page_config(page_title="MODINEMATH COSMOS", page_icon="ζ", layout="wide")

# --- 2. سحر الأنيميشن (Sky & Cloud Edition) ---
st.markdown("""
    <style>
    .stApp { background-color: #050505 !important; }
    .zeta-header {
        text-align: center; font-size: 70px; font-weight: 900;
        background: linear-gradient(90deg, #00bcff, #ffffff, #00bcff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 15px rgba(0, 188, 255, 0.6));
    }
    .particle {
        position: fixed; top: 0; font-family: 'serif'; font-weight: bold; font-size: 32px;
        user-select: none; pointer-events: none; z-index: 0;
        animation: float 15s infinite linear, colorChange 6s infinite ease-in-out;
    }
    @keyframes colorChange { 0%, 100% { color: #00bcff; } 50% { color: #ffffff; } }
    @keyframes float { 0% { transform: translateY(110vh) rotate(0deg); opacity: 0; } 100% { transform: translateY(-10vh) rotate(720deg); opacity: 0; } }
    .response-container {
        color: #ffffff; background: rgba(255,255,255,0.05); 
        padding: 30px; border-radius: 15px; width: 100%; margin-top: 20px;
        border-left: 5px solid #00bcff;
    }
    </style>
    <div class="particle" style="left:10%; animation-duration: 12s;">∫</div>
    <div class="particle" style="left:40%; animation-duration: 18s;">ζ</div>
    <div class="particle" style="left:70%; animation-duration: 14s;">∞</div>
    """, unsafe_allow_html=True)

# --- 3. إعداد العقول (APIs) ---
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# إعداد Gemini للملفات الضخمة
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-pro')

# دالة DeepSeek-R1 (عبر Groq) للذكاء الرياضي
def solve_with_deepseek(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "deepseek-r1-distill-llama-70b", # المحرك الرياضي الجديد
        "messages": [{"role": "system", "content": "You are MODINEMATH. Provide rigorous step-by-step proofs using LaTeX."},
                     {"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        return response.json()['choices'][0]['message']['content']
    except: return "Error connecting to DeepSeek-R1 via Groq."

# --- 4. واجهة المستخدم ---
st.markdown('<div class="zeta-header">ζ MODINEMATH</div>', unsafe_allow_html=True)

uploaded_files = st.file_uploader("Upload large math docs (PDF, Image, etc.)", accept_multiple_files=True)
user_input = st.text_area("", placeholder="Ask the Cosmic AI...", height=120)

if st.button("IGNITE SOLVER ✨"):
    if user_input or uploaded_files:
        with st.spinner("Analyzing the Universe..."):
            # منطق الهجين: إذا كان كاين ملف، Gemini كيحللو، وإذا كان سؤال، DeepSeek كيبرهن
            final_response = ""
            
            if uploaded_files:
                # معالجة الملفات عبر Gemini 1.5 Pro
                combined_content = [user_input]
                for f in uploaded_files:
                    bytes_data = f.read()
                    combined_content.append({"mime_type": f.type, "data": bytes_data})
                
                response = gemini_model.generate_content(combined_content)
                final_response = response.text
            else:
                # حل المسائل الرياضية بـ DeepSeek-R1
                final_response = solve_with_deepseek(user_input)

            # عرض النتيجة
            st.markdown(f'<div class="response-container">{final_response}</div>', unsafe_allow_html=True)

            # بوطونة تحميل PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, txt=final_response.encode('latin-1', 'replace').decode('latin-1'))
            st.download_button("📥 Download PDF Solution", data=pdf.output(dest='S').encode('latin-1'), file_name="Solution.pdf")

st.markdown("<p style='text-align:center; color:rgba(255,255,255,0.1);'>V14.0 | R1 + Gemini Pro Hybrid | Youness Modine</p>", unsafe_allow_html=True)
