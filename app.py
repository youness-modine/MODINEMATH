import streamlit as st
import requests
import json
import fitz
from fpdf import FPDF
import base64

# --- 1. إعدادات PDF الاحترافية ---
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.set_text_color(0, 210, 255)
        self.cell(0, 10, 'MODINEMATH AI - OFFICIAL PROOF', 0, 1, 'C')
        self.line(10, 25, 200, 25)
        self.ln(10)

# --- 2. تصميم واجهة Gemini (CSS Custom Styling) ---
st.set_page_config(page_title="MODINEMATH AI", page_icon="ζ", layout="wide")

st.markdown("""
    <style>
    /* خلفية Gemini العميقة */
    .stApp {
        background-color: #131314;
        color: #e3e3e3;
        font-family: 'Google Sans', sans-serif;
    }
    
    /* العنوان والشعار (Zeta + MODINEMATH) */
    .gemini-header {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
        padding: 20px;
        margin-top: 50px;
    }
    
    .zeta-symbol {
        font-size: 50px;
        background: linear-gradient(to right, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }

    .brand-name {
        font-size: 40px;
        font-weight: 500;
        color: #e3e3e3;
    }

    /* صندوق الإدخال (Chat Input Style) */
    .stTextArea textarea {
        background-color: #1e1f20 !important;
        border: 1px solid #3c4043 !important;
        border-radius: 24px !important;
        color: #e3e3e3 !important;
        padding: 20px !important;
        font-size: 16px !important;
    }

    /* أزرار Gemini */
    div.stButton > button {
        background-color: #1e1f20;
        color: #c4c7c5;
        border: 1px solid #3c4043;
        border-radius: 20px;
        transition: 0.3s;
    }
    
    div.stButton > button:hover {
        background-color: #3c4043;
        border-color: #4285f4;
        color: white;
    }

    /* تنسيق الحلول (Response Box) */
    .response-container {
        background-color: transparent;
        border-left: 3px solid #4285f4;
        padding-left: 20px;
        margin-top: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. محرك Groq (The Global Mathematician) ---
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

def generate_gemini_response(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    
    # البرومبت دابا ذكي: كيعرف اللغة من السؤال نيت (الصينية، اليابانية، إلخ)
    system_prompt = (
        "You are MODINEMATH, an elite mathematician and encyclopedia. "
        "Analyze the user's prompt. If they specify a language like [Chinese] or [Japanese] at the end, "
        "provide the full rigorous proof and explanation in that specific language. "
        "Always use LaTeX for mathematical formulas."
    )
    
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": system_prompt},
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

# --- 4. واجهة المستخدم النهائية ---
st.markdown(f'''
    <div class="gemini-header">
        <span class="zeta-symbol">ζ</span>
        <span class="brand-name">MODINEMATH</span>
    </div>
''', unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#c4c7c5;'>Enter your LaTeX or math question. Example: Define Hilbert Space [Chinese]</p>", unsafe_allow_html=True)

# صندوق البحث (مثل Gemini)
user_input = st.text_area("", placeholder="Ask MODINEMATH anything...", height=100)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    submit_btn = st.button("Generate Solution ✨")

if submit_btn and user_input:
    full_response = ""
    st.markdown('<div class="response-container">', unsafe_allow_html=True)
    ans_area = st.empty()
    
    # الرد اللحظي (Streaming)
    for chunk in generate_gemini_response(user_input):
        full_response += chunk
        ans_area.markdown(full_response + "▌")
    ans_area.markdown(full_response)
    st.markdown('</div>', unsafe_allow_html=True)

    # تصدير الـ PDF
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, full_response.encode('latin-1', 'replace').decode('latin-1'))
    st.download_button("📥 Download Official Proof (PDF)", pdf.output(dest='S').encode('latin-1'), "MODINEMATH_Proof.pdf")

# إضافة ميزة رفع الملفات (Gemini Style)
st.markdown("---")
with st.expander("📎 Upload Documents (PDF/Images)"):
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "png", "jpg"])
    if uploaded_file:
        st.success("File uploaded successfully. Ask your question above about this file.")

st.markdown("<br><br><p style='text-align:center; color:#444746;'>MODINEMATH AI - Version 11.0 (Gemini Interface)</p>", unsafe_allow_html=True)
