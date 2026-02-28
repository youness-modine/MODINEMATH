import streamlit as st
import requests
import google.generativeai as genai
from fpdf import FPDF

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MODINEMATH COSMOS", page_icon="ζ", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505 !important; }
    .zeta-header {
        text-align: center; font-size: 70px; font-weight: 900;
        background: linear-gradient(90deg, #00bcff, #ffffff, #00bcff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 15px rgba(0, 188, 255, 0.6));
    }
    .response-container {
        color: #ffffff; background: rgba(255,255,255,0.05); 
        padding: 30px; border-radius: 15px; width: 100%; margin-top: 20px;
        border-left: 5px solid #00bcff; font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. إعداد العقول (APIs) ---
# تأكد من وضع السوارت بشكل صحيح في Secrets (سطر واحد لكل ساروت)
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=GEMINI_API_KEY)

# استخدام التسمية الأكثر استقراراً لتفادي خطأ 404
# جربنا 'gemini-1.5-pro-latest' و 'models/gemini-1.5-pro'، هادي هي اللي غاتخدم دابا:
gemini_model = genai.GenerativeModel('gemini-1.5-pro')

def solve_with_deepseek(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "deepseek-r1-distill-llama-70b",
        "messages": [{"role": "system", "content": "You are MODINEMATH. Provide rigorous step-by-step math proofs in French or English with LaTeX."},
                     {"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()['choices'][0]['message']['content']

# --- 3. الواجهة ---
st.markdown('<div class="zeta-header">ζ MODINEMATH</div>', unsafe_allow_html=True)

uploaded_files = st.file_uploader("Upload math docs (PDF, Images)", type=['pdf', 'png', 'jpg', 'jpeg'], accept_multiple_files=True)
user_input = st.text_area("", placeholder="Describe your math problem or ask about the files...", height=120)

if st.button("IGNITE SOLVER ✨"):
    if user_input or uploaded_files:
        with st.spinner("Analyzing the Cosmic Data..."):
            try:
                if uploaded_files:
                    # بناء المحتوى لـ Gemini
                    contents = []
                    # إضافة النص أولاً كتعليمات واضحة
                    prompt_text = user_input if user_input else "Analyse ce document mathématique et résous les exercices de manière détaillée."
                    contents.append(prompt_text)
                    
                    for f in uploaded_files:
                        file_bytes = f.read()
                        contents.append({
                            "mime_type": f.type,
                            "data": file_bytes
                        })
                    
                    # طلب الحل من Gemini مع معالجة الأخطاء المباشرة
                    response = gemini_model.generate_content(contents)
                    final_ans = response.text
                else:
                    # طلب الحل من DeepSeek-R1 (عبر Groq)
                    final_ans = solve_with_deepseek(user_input)
                
                st.markdown(f'<div class="response-container">{final_ans}</div>', unsafe_allow_html=True)
                
                # إنشاء ملف PDF للتحميل
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                # تنظيف النص ليتناسب مع ترميز Latin-1
                clean_text = final_ans.encode('latin-1', 'replace').decode('latin-1')
                pdf.multi_cell(0, 10, txt=clean_text)
                st.download_button("📥 Download Solution PDF", data=pdf.output(dest='S').encode('latin-1'), file_name="MODINEMATH_Solution.pdf")
            
            except Exception as e:
                # عرض الخطأ بشكل مفصل للمساعدة في التشخيص
                st.error(f"Cosmos Connection Error: {str(e)}")
                st.info("Tip: If you see 404, check the model name in the code or the API key in Secrets.")

st.markdown("<p style='text-align:center; color:rgba(255,255,255,0.1);'>V14.4 | Final Stable Hybrid | Youness Modine</p>", unsafe_allow_html=True)
