import streamlit as st
import requests
import google.generativeai as genai

# --- 1. جلب وتنظيف السوارت (حماية من الفراغات) ---
GROQ_KEY = st.secrets["GROQ_API_KEY"].strip().replace("\n", "").replace(" ", "")
GEMINI_KEY = st.secrets["GEMINI_API_KEY"].strip().replace("\n", "").replace(" ", "")

# --- 2. إعداد Gemini ---
genai.configure(api_key=GEMINI_KEY)
# التعديل لضمان التوافق مع v1beta
gemini_model = genai.GenerativeModel('gemini-1.5-pro')

def solve_with_deepseek(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "deepseek-r1-distill-llama-70b",
        "messages": [{"role": "system", "content": "You are MODINEMATH. Use LaTeX for math proofs."},
                     {"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    return response.json()['choices'][0]['message']['content']

# --- 3. الواجهة ---
st.markdown("<h1 style='text-align: center; color: #00bcff;'>ζ MODINEMATH</h1>", unsafe_allow_html=True)

uploaded_files = st.file_uploader("Upload TD (PDF/Images)", type=['pdf', 'png', 'jpg', 'jpeg'], accept_multiple_files=True)
user_input = st.text_area("Question:", height=100)

if st.button("IGNITE SOLVER ✨"):
    if user_input or uploaded_files:
        with st.spinner("Analyzing the Cosmos..."):
            try:
                if uploaded_files:
                    # بناء قائمة المحتوى بشكل صحيح لـ Gemini
                    contents = []
                    prompt_text = user_input if user_input else "Analyse ce document et résous les exercices."
                    contents.append(prompt_text)
                    
                    for f in uploaded_files:
                        contents.append({"mime_type": f.type, "data": f.read()})
                    
                    # استدعاء الموديل
                    response = gemini_model.generate_content(contents)
                    final_ans = response.text
                else:
                    final_ans = solve_with_deepseek(user_input)
                
                st.markdown(f'<div style="color:white; background:#111; padding:20px; border-radius:10px;">{final_ans}</div>', unsafe_allow_html=True)
            except Exception as e:
                # إذا رجع الخطأ 404، غانعرفو بلي المشكل في الساروت أو الموديل
                st.error(f"Cosmos Error: {str(e)}")
