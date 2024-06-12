import streamlit as st
from openai import OpenAI

apikey = st.text_input("api key를 입력하세요", type="password")

st.header("음식 메뉴 추천")
prompti = st.text_input("키워드")

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
