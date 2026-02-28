import streamlit as st
import requests
import json
import fitz
from fpdf import FPDF
import base64

# --- 1. إعدادات PDF مطورة (تدعم الأجوبة الطويلة) ---
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.set_text_color(0, 210, 255)
        self.cell(0, 10, 'MODINEMATH AI - OFFICIAL PROOF', 0, 1, 'C')
        self.line(10, 25, 200, 25)
        self.ln(10)

# --- 2. واجهة المستخدم (The Encyclopedia Style) ---
st.set_page_config(page_title="MODINEMATH AI", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at 20% 20%, #1a1c2c, #050505); color: #e0e0e0; }
    .main-title { font-size: 60px; font-weight: 900; background: linear-gradient(90deg, #00d2ff, #92fe9d);
                 -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; }
    .stTextArea textarea { background-color: #0d1117; color: white; border: 1px solid #00d2ff; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🛡️ MODINEMATH ENCYCLOPEDIA</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#8892b0;">The World\'s Most Powerful Mathematical Intelligence</p>', unsafe_allow_html=True)

# --- 3. محرك Groq (الذكاء العالمي) ---
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

def ask_modinemath(prompt, lang, level):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": f"You are MODINEMATH, the world's best mathematician and encyclopedia. Solve or define with rigor in {lang} at {level} level. Use LaTeX."},
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

# --- 4. خيارات المستخدم ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/library.png", width=80)
    lang = st.selectbox("🌐 Language", ["French", "Arabic", "English", "Russian", "Chinese"])
    level = st.radio("Academic Rigor", ["Licence", "Master (MMP)", "Doctorate"])
    st.info("Status: Encyclopedia Mode Active")

# --- 5. منطقة العمل الرئيسية ---
tab1, tab2 = st.tabs(["🧠 Ask Encyclopedia", "📄 Upload & Solve"])

with tab1:
    user_query = st.text_area("Write your math question or define a concept (e.g., Espace de Hilbert):", height=150)
    if st.button("🔍 Search Encyclopedia"):
        if user_query:
            full_ans = ""
            display_area = st.empty()
            for chunk in ask_modinemath(user_query, lang, level):
                full_ans += chunk
                display_area.markdown(full_ans + "▌")
            display_area.markdown(full_ans)
            
            # زر التحميل بعد العرض
            pdf = PDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, full_ans.encode('latin-1', 'replace').decode('latin-1'))
            st.download_button("📥 Save this Definition (PDF)", pdf.output(dest='S').encode('latin-1'), f"Definition_{lang}.pdf")

with tab2:
    uploaded_file = st.file_uploader("Upload PDF Exercise", type=["pdf"])
    if uploaded_file and st.button("🚀 Analyze & Solve"):
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        context = "\n".join([page.get_text() for page in doc])
        if context.strip():
            full_ans_pdf = ""
            display_area_pdf = st.empty()
            for chunk in ask_modinemath(f"Analyze this file content: {context}", lang, level):
                full_ans_pdf += chunk
                display_area_pdf.markdown(full_ans_pdf + "▌")
            display_area_pdf.markdown(full_ans_pdf)
            
            pdf_out = PDF()
            pdf_out.add_page()
            pdf_out.set_font("Arial", size=12)
            pdf_out.multi_cell(0, 10, full_ans_pdf.encode('latin-1', 'replace').decode('latin-1'))
            st.download_button("📥 Download Full Solution (PDF)", pdf_out.output(dest='S').encode('latin-1'), f"Solution_{lang}.pdf")

st.markdown("---")
st.caption("© 2026 MODINEMATH - Developed by Youness Modine | UIT Mathematics Dept.")
