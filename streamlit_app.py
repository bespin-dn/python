import streamlit as st 
import requests

# FastAPI 서버 주소
FASTAPI_URL = "http://127.0.0.1:8000"  # FastAPI가 실행 중인 URL


# KMS 키 목록 가져오기 함수
def fetch_kms_keys():
    try:
        response = requests.get(f"{FASTAPI_URL}/kms/keys")
        if response.status_code == 200:
            return response.json().get("keys", [])  # 키 리스트 반환
        else:
            return ["Error fetching keys"]  # 오류 발생 시 기본값 반환
    except requests.exceptions.RequestException:
        return ["Connection error"]  # FastAPI 연결 오류 처리

# KMS 키 목록 동적 설정
KMS_KEYS = fetch_kms_keys()
KMS_KEYS = [f"{key['Alias'].replace('alias/','')} ({key['KeyId']})" for key in KMS_KEYS]  # 출력 형식 변경


st.set_page_config(page_title="Bespinglobal", layout="wide")

# KMS 탭 생성
tab1, tab2 = st.tabs(["🔐 KMS", "🤖 GenAI"])

with tab1:
    # **최상단에 KMS Key 선택 Selectbox 추가**
    selected_key = st.selectbox("🔑 Select KMS Key", KMS_KEYS)

    # 중앙 입력 박스
    plaintext = st.text_area("🔤 Enter text", height=100)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔒 Encrypt"):
            if plaintext:
                response = requests.post(f"{FASTAPI_URL}/encrypt", json={"key": selected_key, "text": plaintext})
                if response.status_code == 200:
                    encrypted_text = response.json().get("encrypted_text", "")
                    st.success("✅ Encryption Successful!")
                    st.code(encrypted_text, language="plaintext")
                else:
                    st.error("❌ Encryption failed.")
            else:
                st.warning("⚠️ Please enter text to encrypt.")

    with col2:
        if st.button("🔓 Decrypt"):
            if plaintext:
                response = requests.post(f"{FASTAPI_URL}/decrypt", json={"key": selected_key, "text": plaintext})
                if response.status_code == 200:
                    decrypted_text = response.json().get("decrypted_text", "")
                    st.success("✅ Decryption Successful!")
                    st.code(decrypted_text, language="plaintext")
                else:
                    st.error("❌ Decryption failed.")
            else:
                st.warning("⚠️ Please enter encrypted text to decrypt.")
