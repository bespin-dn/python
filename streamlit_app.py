import streamlit as st
import requests

# FastAPI 서버 주소
FASTAPI_URL = "http://127.0.0.1:8000"  # FastAPI가 실행 중인 URL

st.title("FastAPI와 Streamlit 연동")

# 사용자 입력 받기
msg = st.text_input("메시지를 입력하세요:")

# 버튼 클릭 시 FastAPI에 POST 요청 보내기
if st.button("전송"):
    response = requests.post(f"{FASTAPI_URL}/", params={"msg": msg})
    
    if response.status_code == 200:
        result = response.json()
        st.success(f"응답: {result['msg']}")
    else:
        st.error("FastAPI 요청 실패")
