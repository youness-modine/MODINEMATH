import streamlit as st
import requests
import json
from streamlit_lottie import st_lottie
import time

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MODINE COPILOT", page_icon="🚀", layout="wide")

# دالة تحميل الأنيميشن مع الحماية
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        return r.json() if r.status_code == 200 else None
    except: return None

lottie_ai = load_lottieurl("https://lottie.host/8e202975-5282-4f72-9658-54c30c3331b2/pP6eFw6z7B.json")

# --- 2. الذاكرة (Chat History Initializer) ---
# هاد الجزء هو اللي كيخلي السيت يعقل عليك
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. تصميم الواجهة (DeepSeek Dark Mode) ---
st.markdown("""
    <style>
    .stApp { background: #0b0b0d !important; }
    .stApp::before {
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: transparent url('https://www.transparenttextures.com/patterns/stardust.png') repeat;
        opacity: 0.2; z-index: -1; animation: move-twinkle 200s linear infinite;
    }
    @keyframes move-twinkle { from { background-position: 0 0; } to { background-position: -10000px 5000px; } }
    
    /* تنسيق فقاعات الدردشة */
    .chat-bubble { padding: 15px; border-radius: 15px; margin-bottom: 10px; max-width: 85%; }
    .user-bubble { background: #1e1f20; color: white; align-self: flex-end; border-bottom-right-radius: 2px; }
    .ai-bubble { background: rgba(66, 133, 244, 0.1); color: #e3e3e3; border-left: 3px solid #4285f4; border-bottom-left-radius: 2px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. محرك Groq مع دعم الذاكرة ---
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

def get_ai_response(messages):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "system", "content": "You are MODINE COPILOT, a top-tier math AI. Use LaTeX and maintain context."}] + messages,
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

# --- 5. واجهة المستخدم ---
col_l, col_r = st.columns([1, 5])
with col_l:
    if lottie_ai: st_lottie(lottie_ai, height=80, key="ai_icon")
    else: st.write("🚀")
with col_r:
    st.markdown("<h1 style='color:white; margin:0;'>MODINE COPILOT</h1>", unsafe_allow_html=True)

# عرض الحوار القديم (Display History)
# هادي هي اللي كاتخليك تشوف شنو سولتي قبل
for message in st.session_state.messages:
    div_class = "user-bubble" if message["role"] == "user" else "ai-bubble"
    st.markdown(f'<div class="chat-bubble {div_class}">{message["content"]}</div>', unsafe_allow_html=True)

# منطقة الإدخال (Chat Input مثل DeepSeek)
if prompt := st.chat_input("Ask MODINE COPILOT..."):
    # تخزين سؤال المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # توليد رد الذكاء الاصطناعي
    with st.chat_message("assistant", avatar="🛡️"):
        res_placeholder = st.empty()
        full_res = ""
        for chunk in get_ai_response(st.session_state.messages):
            full_res += chunk
            res_placeholder.markdown(full_res + "▌")
        res_placeholder.markdown(full_res)
    
    # تخزين رد الذكاء في الذاكرة
    st.session_state.messages.append({"role": "assistant", "content": full_res})

st.markdown("<p style='text-align:center; color:#444746; margin-top:50px;'>Neural Memory V14.0 | Powered by Groq</p>", unsafe_allow_html=True)
