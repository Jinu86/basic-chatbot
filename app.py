import os
import streamlit as st
import google.generativeai as genai

# 환경변수에서 Gemini API 키 로드
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"] if "GOOGLE_API_KEY" in st.secrets else os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Gemini 모델 초기화
model = genai.GenerativeModel("gemini-pro")

# Streamlit 페이지 설정
st.set_page_config(page_title="Gemini Chatbot", page_icon="💬", layout="centered")

# 앱 제목
st.title("💬 Gemini Chatbot Template")

# 기능 설명
with st.expander("ℹ️ 사용법"):
    st.markdown("""
    - 텍스트 입력 후 `Enter` 또는 `전송` 버튼 클릭
    - Google Gemini API를 사용하여 답변 생성
    - 이전 대화는 화면에 유지됩니다
    """)

# 세션 상태 초기화 (대화 저장용)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 기존 대화 기록 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력
if prompt := st.chat_input("메시지를 입력하세요"):
    # 사용자 메시지 출력
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # Gemini API 호출
        response = model.generate_content(prompt)
        reply = response.text

        # Gemini 응답 출력
        st.chat_message("assistant").markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

    except Exception as e:
        st.error(f"에러 발생: {e}")
