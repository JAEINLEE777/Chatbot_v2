import streamlit as st
from openai import OpenAI
from datetime import datetime
import pytz

# 페이지 설정
st.set_page_config(page_title="💬 한국 시간 채팅봇", layout="wide")

# 사용자 정의 CSS 추가
st.markdown("""
<style>
    .stChat {
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    .user {
        background-color: #e6f3ff;
        text-align: right;
    }
    .assistant {
        background-color: #f0f0f0;
    }
    .timestamp {
        font-size: 0.8em;
        color: #888;
    }
</style>
""", unsafe_allow_html=True)

# 한국 시간대 설정
korea_tz = pytz.timezone('Asia/Seoul')

# 현재 한국 시간을 반환하는 함수
def get_korea_time():
    return datetime.now(korea_tz).strftime("%Y-%m-%d %H:%M:%S")

# 사이드바 설정
with st.sidebar:
    st.title("채팅 설정")
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[OpenAI API 키 받기](https://platform.openai.com/account/api-keys)"
    "[소스 코드 보기](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![GitHub Codespaces에서 열기](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

# 메인 앱 제목
st.title("💬 한국 시간 채팅봇")

# 세션 상태에 메시지 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "무엇을 도와드릴까요?", "timestamp": get_korea_time()}]

# 저장된 메시지 표시
for msg in st.session_state.messages:
    with st.container():
        col1, col2 = st.columns([0.85, 0.15])
        with col1:
            st.markdown(f"<div class='stChat {msg['role']}'>{msg['content']}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='timestamp'>{msg['timestamp']}</div>", unsafe_allow_html=True)

# 사용자 입력 받기
if prompt := st.chat_input("메시지를 입력하세요..."):
    # API 키 확인
    if not openai_api_key:
        st.info("계속하려면 OpenAI API 키를 추가해주세요.")
        st.stop()

    # OpenAI 클라이언트 초기화
    client = OpenAI(api_key=openai_api_key)

    # 현재 한국 시간 가져오기
    current_time = get_korea_time()

    # 사용자 메시지를 세션 상태에 추가
    st.session_state.messages.append({"role": "user", "content": prompt, "timestamp": current_time})
    
    # 사용자 메시지 표시
    with st.container():
        col1, col2 = st.columns([0.85, 0.15])
        with col1:
            st.markdown(f"<div class='stChat user'>{prompt}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='timestamp'>{current_time}</div>", unsafe_allow_html=True)

    # OpenAI API를 사용하여 응답 생성
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content

    # 응답 시간 가져오기
    response_time = get_korea_time()

    # 응답을 세션 상태에 추가하고 화면에 표시
    st.session_state.messages.append({"role": "assistant", "content": msg, "timestamp": response_time})
    
    with st.container():
        col1, col2 = st.columns([0.85, 0.15])
        with col1:
            st.markdown(f"<div class='stChat assistant'>{msg}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='timestamp'>{response_time}</div>", unsafe_allow_html=True)

# 스크롤을 최신 메시지로 이동
st.container().markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
