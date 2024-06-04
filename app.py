import streamlit as st
import openai

# OpenAI API 키 입력 받기
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password", key="api_key")

# OpenAI API 초기화
openai.api_key = api_key

# 사용자의 질문을 입력 받아 GPT-3.5-Turbo 모델의 응답을 출력하는 함수 정의
@st.cache
def generate_response(question):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question,
        max_tokens=50
    )
    return response.choices[0].text.strip()

# 메인 Streamlit 애플리케이션
def main():
    st.title("GPT-3.5 Turbo Web App")

    # 사용자에게 질문 입력 받기
    question = st.text_input("Enter your question here:")

    # 질문이 입력되었을 때만 답변 생성
    if question:
        # GPT-3.5-Turbo 모델을 사용하여 응답 생성
        response = generate_response(question)
        
        # 생성된 응답 출력
        st.write("AI's response:")
        st.write(response)

if __name__ == "__main__":
    main()
