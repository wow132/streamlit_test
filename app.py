import streamlit as st
import openai

# OpenAI API 키 입력 받기
def get_openai_api_key():
    api_key = st.session_state.get("api_key", "")
    api_key = st.text_input("OpenAI API 키를 입력하세요:", value=api_key, type="password")
    st.session_state["api_key"] = api_key
    return api_key

# OpenAI API 초기화
def init_openai():
    api_key = get_openai_api_key()
    openai.api_key = api_key

# DALL-E로 이미지 생성
def generate_image(prompt):
    response = openai.Image.create(
        model="clip-dalle-1619",
        prompts=[prompt],
        image_width=512,
        image_height=512,
    )
    return response.url

# 새 페이지 설정
def dall_e_page():
    st.title("DALL-E 이미지 생성")
    
    init_openai()  # OpenAI 초기화
    
    # 사용자 프롬프트 입력 받기
    prompt = st.text_area("프롬프트를 입력하세요:")
    
    if st.button("이미지 생성"):
        if prompt:
            image_url = generate_image(prompt)
            st.image(image_url, caption="생성된 이미지", use_column_width=True)
        else:
            st.warning("프롬프트를 입력하세요.")

# 메인 애플리케이션
def main():
    st.sidebar.title("네비게이션")
    selection = st.sidebar.radio("이동", ["Q&A", "DALL-E 이미지 생성"])

    if selection == "Q&A":
        qna_page()
    elif selection == "DALL-E 이미지 생성":
        dall_e_page()

if __name__ == "__main__":
    main()
