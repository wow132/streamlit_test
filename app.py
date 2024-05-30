
import streamlit as st
from openai import OpenAI
import openai
pip install --upgrade openai

# OpenAI API 키 입력 받기
def get_openai_api_key():
    api_key = st.session_state.get("api_key", "")
    api_key = st.text_input("Enter your OpenAI API Key:", value=api_key, type="password")
    st.session_state["api_key"] = api_key
    return api_key

# OpenAI API 초기화
def init_openai():
    api_key = get_openai_api_key()
    openai.api_key = api_key

# DALL-E로 이미지 생성
@st.cache
def generate_image(prompt):
    response = openai.Image.create(
        engine="dalle",
        prompt=prompt,
        max_images=1
    )
    return response.images[0].url

# 새 페이지 설정
def dall_e_page():
    st.title("DALL-E Image Generation")
    
    init_openai()  # OpenAI 초기화
    
    # 사용자 프롬프트 입력 받기
    prompt = st.text_area("Enter your prompt:")
    
    if st.button("Generate Image"):
        if prompt:
            image_url = generate_image(prompt)
            st.image(image_url, caption="Generated Image", use_column_width=True)
        else:
            st.warning("Please enter a prompt.")

# 메인 애플리케이션
def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", ["Q&A", "DALL-E Image Generation"])

    if selection == "Q&A":
        qna_page()
    elif selection == "DALL-E Image Generation":
        dall_e_page()

if __name__ == "__main__":
    main()
