
import streamlit as st
from openai import OpenA
import openai

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

# 질문에 대한 GPT-3.5 Turbo 응답 생성
def generate_response(question):
    response = openai.Completion.create(
        engine="text-davinci-003",  # GPT-3.5 Turbo 엔진 선택
        prompt=question,
        max_tokens=150,  # 응답의 최대 길이 설정
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Streamlit 애플리케이션 설정
def main():
    st.title("GPT-3.5 Turbo Q&A Web App")
    
    init_openai()  # OpenAI 초기화
    
    # 사용자 질문 입력 받기
    question = st.text_area("Enter your question:")
    
    if st.button("Get Answer"):
        if question:
            answer = generate_response(question)
            st.write("Answer:", answer)
        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main()
