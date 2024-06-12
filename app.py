import streamlit as st
from openai import OpenAI

apikey = st.text_input("api key를 입력하세요", type="password")

st.header("음식 메뉴 추천")
prompti = st.text_input("키워드")
def food_recommendation():
    st.title("음식 추천기")
    
    st.write("음식을 추천받고 싶으신가요? 몇 가지 질문에 답해주세요!")
    
    craving = st.selectbox("지금 먹고 싶은 음식의 유형을 선택하세요:", ["Salty", "Sweet", "Not sure"])
    meal_type = st.selectbox("어느 식사 시간에 대한 추천을 원하시나요?", ["Breakfast", "Lunch", "Dinner"])
    
    answers = {'craving': craving.lower(), 'meal_type': meal_type.lower()}

@st.cache_data()
def draw(prompt):
    client = OpenAI(api_key=apikey)
    response = client.images.generate(model="dall-e-3",prompt=f'{prompt}와 관련된 음식 메뉴 하나를 그려줘')
    image_url = response.data[0].url
    image = f"![alt text]({image_url})"
    return image
   
if st.button("start"):
  img = draw(prompti)
  st.markdown(img)
