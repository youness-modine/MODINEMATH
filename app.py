import streamlit as st
import requests
import google.generativeai as genai
from fpdf import FPDF

# --- 1. جلب وتنظيف السوارت أوتوماتيكياً ---
try:
    # هاد العملية كتحيد أي Enter أو Space زايد في السوارت
    GROQ_KEY = st.secrets["GROQ_API_KEY"].strip().replace("\n", "").replace(" ", "")
    GEMINI_KEY = st.secrets["GEMINI_API_KEY"].strip().replace("\n", "").replace(" ", "")
except Exception as e:
    st.error("Missing API Keys in Secrets!")
    st.stop()

# --- 2. إعداد العقول ---
genai.configure(api_key=GEMINI_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-pro')

def solve_with_deepseek(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "deepseek-r1-distill-llama-70b",
        "messages": [{"role": "system", "content": "You are MODINEMATH. Solve math with detailed LaTeX proofs."},
                     {"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Groq Error {response.status_code}: {response.text}"

# --- 3. الواجهة ---
st.markdown("<h1 style='text-align: center; color: #00bcff;'>ζ MODINEMATH</h1>", unsafe_allow_html=True)

uploaded_files = st.file_uploader("Upload Math TD (PDF/Images)", type=['pdf', 'png', 'jpg', 'jpeg'], accept_multiple_files=True)
user_input = st.text_area("Question/Prompt:", placeholder="Describe the math problem...", height=100)

if st.button("IGNITE SOLVER ✨"):
    if user_input or uploaded_files:
        with st.spinner("Processing the Cosmic Knowledge..."):
            try:
                if uploaded_files:
                    # استخدام Gemini للملفات
                    contents = [user_input if user_input else "Analyse et résous."]
                    for f in uploaded_files:
                        contents.append({"mime_type": f.type, "data": f.read()})
                    response = gemini_model.generate_content(contents)
                    final_ans = response.text
                else:
                    # استخدام DeepSeek-R1 للنصوص
                    final_ans = solve_with_deepseek(user_input)
                
                st.markdown(f'<div style="color:white; background:#111; padding:20px; border-radius:10px; border-left:5px solid #00bcff;">{final_ans}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.markdown("<p style='text-align:center; color:gray; font-size:10px;'>V15.0 | New Key Auth | Youness Modine</p>", unsafe_allow_html=True)
