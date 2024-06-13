import streamlit as st
import openai
import requests
from bs4 import BeautifulSoup

# DALL-E를 사용하여 이미지를 생성하는 함수
def draw(client, prompt):
    response = client.Image.create(prompt=prompt, n=1, size="1024x1024")
    image_url = response['data'][0]['url']
    image = f"![alt text]({image_url})"
    return image

# URL에서 데이터를 가져와 텍스트로 변환하는 함수
def download_and_extract_text(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    return text

# Streamlit 앱의 헤더와 입력 폼
st.header("음식 메뉴 추천")

apikey = st.text_input("API key를 입력하세요", type="password")

if apikey:
    openai.api_key = apikey
    client = openai
    
    prompti = st.text_input("키워드")

    if st.button("start"):
        try:
            # 지정된 URL에서 텍스트 데이터를 추출
            url = "https://www.diningcode.com/list.dc?query=부산맛집"
            extracted_text = download_and_extract_text(url)

            # OpenAI API를 사용하여 추천 음식 생성
            response = client.Completion.create(
                engine="text-davinci-003",
                prompt=f"{prompti}와 관련된 음식 한가지를 추천해줘. 여기 텍스트를 참고해: {extracted_text}",
                max_tokens=150
            )
            r = response.choices[0].text.strip()
            st.markdown(r)

            # DALL-E를 사용하여 이미지 생성
            img = draw(client, r)
            st.markdown(img)
        except openai.error.AuthenticationError:
            st.error("API 키 인증에 실패했습니다. 올바른 API 키를 입력하세요.")
        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")
