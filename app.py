import streamlit as st
import requests
import json
import fitz  # PyMuPDF
from fpdf import FPDF
from PIL import Image
import pandas as pd
import docx
import io

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MODINEMATH COSMOS", page_icon="ζ", layout="wide")

# --- 2. سحر الأنيميشن (Sky & Cloud Edition) ---
st.markdown("""
    <style>
    .stApp { background-color: #050505 !important; }
    .zeta-header {
        text-align: center;
        font-size: 70px; font-weight: 900;
        background: linear-gradient(90deg, #00bcff, #ffffff, #00bcff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 15px rgba(0, 188, 255, 0.6));
    }
    .particle {
        position: fixed; top: 0; font-family: 'serif'; font-weight: bold;
        font-size: 32px; user-select: none; pointer-events: none; z-index: 0;
        animation: float 15s infinite linear, colorChange 6s infinite ease-in-out;
    }
    @keyframes colorChange { 0%, 100% { color: #00bcff; } 50% { color: #ffffff; } }
    @keyframes float { 0% { transform: translateY(110vh) rotate(0deg); opacity: 0; } 100% { transform: translateY(-10vh) rotate(720deg); opacity: 0; } }
    
    .response-container {
        color: #ffffff; background: rgba(255,255,255,0.05); 
        padding: 30px; border-radius: 15px; width: 100%; margin-top: 20px;
    }
    </style>
    <div class="particle" style="left:10%; animation: float 12s infinite linear;">∫</div>
    <div class="particle" style="left:30%; animation: float 15s infinite linear;">ζ</div>
    <div class="particle" style="left:50%; animation: float 18s infinite linear;">∞</div>
    <div class="particle" style="left:70%; animation: float 14s infinite linear;">Σ</div>
    <div class="particle" style="left:90%; animation: float 16s infinite linear;">π</div>
    """, unsafe_allow_html=True)

# --- 3. محرك Groq المطور ---
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

def generate_cosmos_ans(prompt, context=""):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    full_prompt = f"Context from files: {context}\n\nUser Question: {prompt}"
    payload = {
        "model": "deepseek-r1-distill-llama-70b",
        "messages": [{"role": "system", "content": "You are MODINEMATH, a cosmic math AI. Analyze files and solve with LaTeX."},
                     {"role": "user", "content": full_prompt}]
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        return response.json()['choices'][0]['message']['content'] if response.status_code == 200 else f"Error: {response.text}"
    except Exception as e: return f"Error: {str(e)}"

# --- 4. معالجة أنواع الملفات المختلفة ---
def extract_text(file):
    if file.type == "application/pdf":
        doc = fitz.open(stream=file.read(), filetype="pdf")
        return "\n".join([page.get_text() for page in doc])
    elif file.type in ["image/png", "image/jpeg"]:
        return "[Image detected - AI will analyze visual patterns if possible]"
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(file)
        return "\n".join([p.text for p in doc.paragraphs])
    elif file.type in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "text/csv"]:
        df = pd.read_excel(file) if "sheet" in file.type else pd.read_csv(file)
        return df.to_string()
    return ""

# --- 5. واجهة المستخدم ---
st.markdown('<div class="zeta-header">ζ MODINEMATH</div>', unsafe_allow_html=True)

# منطقة الرفع العالمية (يدعم 5GB بفضل config.toml)
uploaded_files = st.file_uploader("Upload Math Documents (PDF, JPG, PNG, DOCX, Excel)", 
                                  type=["pdf", "png", "jpg", "docx", "xlsx", "csv"], 
                                  accept_multiple_files=True)

user_input = st.text_area("", placeholder="Ask about your files or write a math question...", height=100)

if st.button("IGNITE SOLVER ✨"):
    if user_input or uploaded_files:
        with st.spinner("Processing the Universe..."):
            file_context = ""
            if uploaded_files:
                for f in uploaded_files:
                    file_context += f"\n--- File: {f.name} ---\n" + extract_text(f)
            
            ans = generate_cosmos_ans(user_input, file_context)
            st.markdown(f'<div class="response-container">{ans}</div>', unsafe_allow_html=True)
            
            # ميزة تحميل الحل PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, txt=ans.encode('latin-1', 'replace').decode('latin-1'))
            pdf_output = pdf.output(dest='S').encode('latin-1')
            st.download_button(label="📥 Download Solution as PDF", data=pdf_output, file_name="MODINEMATH_Solution.pdf", mime="application/pdf")

st.markdown("<p style='text-align:center; color:rgba(255,255,255,0.2);'>V13.0 | Universal Solver | Youness Modine</p>", unsafe_allow_html=True)

