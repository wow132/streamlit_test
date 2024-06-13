import streamlit as st
from openai import OpenAI

def draw(prompt):
    response = client.images.generate(model="dall-e-3",prompt= prompt)
    image_url = response.data[0].url
    image = f"![alt text]({image_url})"
    return image

apikey = st.text_input("api key를 입력하세요", type="password")

client = OpenAI(api_key=apikey)

st.header("음식 메뉴 추천")
prompti = st.text_input("키워드")

if st.button("start"):
    response = client.chat.completions.create(
      model="gpt-4o",
      messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f'{prompti}와 관련된 음식 한가지를 추천해줘'},
      ]
    )
    r = response.choices[0].message.content
    st.markdown(r)
    img = draw(r)
    st.markdown(img)
