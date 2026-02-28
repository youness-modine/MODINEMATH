import streamlit as st
import requests
import google.generativeai as genai
from fpdf import FPDF

# --- 1. تنظيف وجلب السوارت ---
# هاد الأسطر غاتحيد أي فراغ أو سطر زايد بشكل أوتوماتيكي
GROQ_API_KEY = st.secrets["GROQ_API_KEY"].replace("\n", "").replace(" ", "").strip()
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"].replace("\n", "").replace(" ", "").strip()

# --- 2. إعداد Gemini ---
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-pro')

def solve_with_deepseek(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "deepseek-r1-distill-llama-70b", # الموديل خدام بساروت Groq
        "messages": [{"role": "system", "content": "You are MODINEMATH. Solve with LaTeX."},
                     {"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Groq Error: {response.status_code} - {response.text}"

# --- 3. الواجهة (MODINEMATH) ---
st.markdown("<h1 style='text-align: center; color: #00bcff;'>ζ MODINEMATH</h1>", unsafe_allow_html=True)

uploaded_files = st.file_uploader("Upload TD (PDF, Images)", type=['pdf', 'png', 'jpg', 'jpeg'], accept_multiple_files=True)
user_input = st.text_area("Ask MODINEMATH...", height=100)

if st.button("IGNITE SOLVER ✨"):
    if user_input or uploaded_files:
        with st.spinner("Analyzing the Cosmos..."):
            try:
                if uploaded_files:
                    contents = [user_input if user_input else "Résous ces exercices."]
                    for f in uploaded_files:
                        contents.append({"mime_type": f.type, "data": f.read()})
                    response = gemini_model.generate_content(contents)
                    final_ans = response.text
                else:
                    final_ans = solve_with_deepseek(user_input)
                
                st.markdown(f'<div style="color: white; background: #111; padding: 20px; border-radius: 10px; border-left: 5px solid #00bcff;">{final_ans}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Cosmos Error: {str(e)}")
