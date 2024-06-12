import streamlit as st
from openai import OpenAI

apikey = st.text_input("API key를 입력하세요", type="password")

st.header("음식 메뉴 추천")
cuisine_choice = st.selectbox("어떤 종류의 음식을 추천 받으시겠습니까?", ["한식", "일식", "중식", "양식"])
prompt_keywords = {
    "한식": ["김치", "비빔밥", "불고기", "된장찌개", "김치찌개"],
    "일식": ["초밥", "라멘", "돈부리", "우동", "오코노미야끼"],
    "중식": ["짜장면", "짬뽕", "탕수육", "양장피", "볶음밥"],
    "양식": ["스테이크", "파스타", "햄버거", "샐러드", "피자"]
}
selected_cuisine = cuisine_choice.lower()
prompti = st.selectbox(f"{selected_cuisine}과(와) 관련된 키워드를 선택하세요:", prompt_keywords[selected_cuisine])

@st.cache_data()
def draw(prompt):
    client = OpenAI(api_key=apikey)
    response = client.images.generate(model="dall-e-3", prompt=f'{prompt}와 관련된 음식 메뉴 하나를 그려줘')
    image_url = response.data[0].url
    image = f"![alt text]({image_url})"
    return image
   
if st.button("시작"):
    img = draw(prompti)
    st.markdown(img)
