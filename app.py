import streamlit as st
import google.generativeai as genai
import os

# -------------------
# 1. 환경 변수 설정
# -------------------
# Streamlit Cloud 사용 시, secrets에 GOOGLE_API_KEY 등록 권장
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))

if not GOOGLE_API_KEY:
    st.error("❌ Google API Key가 설정되지 않았습니다.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# ---------------------
# 2. 모델 초기화
# ---------------------
model = genai.GenerativeModel("gemini-1.5-pro")

# ---------------------
# 3. 세션 상태 초기화
# ---------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# ---------------------
# 4. 제목 및 설명
# ---------------------
st.set_page_config(page_title="Gemini ChatBot", layout="centered")
st.title("🤖 Gemini ChatBot Framework")
st.markdown("""
이 챗봇은 Google Gemini 1.5 Pro API와 Streamlit을 기반으로 구축되었습니다.  
대화 컨텍스트를 기억하고, Streamlit Cloud에서 바로 실행 가능합니다.  
**기본 틀**로 사용하며, 다양한 챗봇 서비스로 확장 가능하도록 설계되어 있습니다.
""")

# ---------------------
# 5. 대화 UI 출력
# ---------------------
for entry in st.session_state.chat_history:
    with st.chat_message(entry["role"]):
        st.markdown(entry["text"])

# ---------------------
# 6. 사용자 입력 처리
# ---------------------
user_input = st.chat_input("무엇이든 물어보세요!")

if user_input:
    # 사용자 메시지 출력 및 기록
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "text": user_input})

    # Gemini 응답 생성
    try:
        response = st.session_state.chat.send_message(user_input)
        bot_reply = response.text
    except Exception as e:
        bot_reply = f"오류 발생: {e}"

    # 응답 메시지 출력 및 기록
    st.chat_message("assistant").markdown(bot_reply)
    st.session_state.chat_history.append({"role": "assistant", "text": bot_reply})
