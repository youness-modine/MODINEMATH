import streamlit as st
import requests
import google.generativeai as genai
from fpdf import FPDF

# --- الإعدادات ---
st.set_page_config(page_title="MODINEMATH COSMOS", layout="wide")

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# إعداد Gemini 
genai.configure(api_key=GEMINI_API_KEY)
# استهداف الموديل بالاسم المختصر والأكثر استقرارا
gemini_model = genai.GenerativeModel('gemini-1.5-pro')

def solve_with_deepseek(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "deepseek-r1-distill-llama-70b",
        "messages": [{"role": "system", "content": "You are MODINEMATH. Solve math with LaTeX."},
                     {"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()['choices'][0]['message']['content']

# --- الواجهة ---
st.markdown("<h1 style='text-align: center; color: #00bcff;'>ζ MODINEMATH</h1>", unsafe_allow_html=True)

uploaded_files = st.file_uploader("Upload TD (PDF, Images)", type=['pdf', 'png', 'jpg', 'jpeg'], accept_multiple_files=True)
user_input = st.text_area("Ask MODINEMATH...", height=100)

if st.button("IGNITE SOLVER ✨"):
    if user_input or uploaded_files:
        with st.spinner("Processing..."):
            try:
                if uploaded_files:
                    contents = [user_input if user_input else "Résous ces exercices mathématiques."]
                    for f in uploaded_files:
                        contents.append({"mime_type": f.type, "data": f.read()})
                    
                    response = gemini_model.generate_content(contents)
                    final_ans = response.text
                else:
                    final_ans = solve_with_deepseek(user_input)
                
                st.markdown(f'<div style="color: white; background: #111; padding: 20px; border-radius: 10px;">{final_ans}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {str(e)}")
