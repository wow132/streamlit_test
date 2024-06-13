import streamlit as st
from openai import OpenAI
import requests
from bs4 import BeautifulSoup

# DALL-E를 사용하여 이미지를 생성하는 함수
def draw(prompt):
    response = client.images.generate(model="dall-e-3", prompt=prompt)
    image_url = response.data[0].url
    image = f"![alt text]({image_url})"
    return image

# URL에서 데이터를 가져와 텍스트로 변환하는 함수
def download_and_extract_text(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    return text

# Streamlit 앱의 헤더와 입력 폼
apikey = st.text_input("API key를 입력하세요", type="password")

if apikey:
    client = OpenAI(api_key=apikey)
    st.header("음식 메뉴 추천")
    prompti = st.text_input("키워드")

    if st.button("start"):
        # 지정된 URL에서 텍스트 데이터를 추출
        url = "https://www.diningcode.com/list.dc?query=%EA%B2%BD%EC%84%B1%EB%8C%80%EB%B6%80%EA%B2%BD%EB%8C%80&order=r_score"
        extracted_text = download_and_extract_text(url)

        # OpenAI API를 사용하여 추천 음식 생성
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f'{prompti}와 관련된 음식 한가지를 추천해줘. 여기 텍스트를 참고해: {extracted_text}'},
            ]
        )
        r = response.choices[0].message.content
        st.markdown(r)

        # DALL-E를 사용하여 이미지 생성
        img = draw(r)
        st.markdown(img)
