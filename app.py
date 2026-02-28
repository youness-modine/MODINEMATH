import streamlit as st
import requests
import json
from streamlit_lottie import st_lottie
import time

# --- 1. إعدادات الصفحة والهوية ---
st.set_page_config(page_title="MODINE COPILOT", page_icon="🚀", layout="wide")

# دالة لتحميل الأنيميشن
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

lottie_ai = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_g3p3re9h.json")

# --- 2. سحر الواجهة (Grok & DeepSeek Style CSS) ---
st.markdown("""
    <style>
    /* خلفية كونية غامقة */
    .stApp {
        background: radial-gradient(circle at center, #0a0a0b 0%, #000000 100%) !important;
    }

    /* أنيميشن النجوم في الخلفية */
    @keyframes move-twinkle {
        from { background-position: 0 0; }
        to { background-position: -10000px 5000px; }
    }
    .stApp::before {
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: transparent url('https://www.transparenttextures.com/patterns/stardust.png') repeat;
        z-index: -1; opacity: 0.3; animation: move-twinkle 200s linear infinite;
    }

    /* صندوق البحث العائم (Floating Input) */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        color: white !important;
        padding: 25px !important;
        font-size: 18px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
    }

    /* أزرار Gemini المتوهجة */
    div.stButton > button {
        background: linear-gradient(90deg, #4285f4, #9b72cb) !important;
        border: none !important;
        border-radius: 12px !important;
        color: white !important;
        font-weight: bold !important;
        padding: 10px 25px !important;
        transition: 0.3s !important;
    }
    
    div.stButton > button:hover {
        box-shadow: 0 0 20px rgba(155, 114, 203, 0.6) !important;
        transform: scale(1.05) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. محرك Groq (الذكاء) ---
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

def get_ai_response(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "system", "content": "You are a professional Copilot. Use LaTeX for math."},
                     {"role": "user", "content": prompt}],
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
st.write("<br><br>", unsafe_allow_html=True)
col_l, col_r = st.columns([1, 4])
with col_l:
    st_lottie(lottie_ai, height=100, key="ai_icon")
with col_r:
    st.markdown("<h1 style='color:white; font-size:45px;'>MODINE COPILOT</h1>", unsafe_allow_html=True)

# منطقة الإدخال المركزية
user_query = st.text_area("", placeholder="What do you want to know?", height=120, label_visibility="collapsed")

c1, c2, c3 = st.columns([1, 0.5, 1])
with c2:
    if st.button("Generate ✨"):
        if user_query:
            full_res = ""
            res_box = st.empty()
            for chunk in get_ai_response(user_query):
                full_res += chunk
                res_box.markdown(f"<div style='background:rgba(255,255,255,0.03); padding:20px; border-radius:15px; border-left:4px solid #9b72cb;'>{full_res}▌</div>", unsafe_allow_html=True)
            res_box.markdown(f"<div style='background:rgba(255,255,255,0.03); padding:20px; border-radius:15px; border-left:4px solid #9b72cb;'>{full_res}</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#444746; margin-top:100px;'>Based on Groq LPU Technology | V13.0</p>", unsafe_allow_html=True)
