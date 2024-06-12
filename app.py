import streamlit as st
from openai import OpenAI

apikey = st.text_input("api key를 입력하세요", type="password")

st.header("음식 메뉴 추천")

# 사용자 선호도를 묻는 질문 추가
food_type = st.selectbox("어떤 종류의 음식을 선호하나요?", ["한식", "중식", "일식", "양식"])
taste_preference = st.selectbox("어떤 맛을 선호하나요?", ["매운 맛", "단 맛", "짠 맛", "신 맛"])
main_ingredient = st.selectbox("주요 재료는 무엇을 선호하나요?", ["고기", "해산물", "채소", "곡류"])

# 추천 음식을 선택하도록 유도
if food_type == "한식":
    if taste_preference == "매운 맛":
        if main_ingredient == "고기":
            prompti = "매운 돼지 불고기"
        elif main_ingredient == "해산물":
            prompti = "매운 해물 찌개"
        elif main_ingredient == "채소":
            prompti = "매운 채소 비빔밥"
        else:
            prompti = "매운 떡볶이"
    elif taste_preference == "단 맛":
        if main_ingredient == "고기":
            prompti = "불고기"
        elif main_ingredient == "해산물":
            prompti = "간장 새우"
        elif main_ingredient == "채소":
            prompti = "잡채"
        else:
            prompti = "호떡"
    # 기타 맛과 재료에 대한 추천을 추가할 수 있습니다
else:
    prompti = f"{food_type} {taste_preference} {main_ingredient}"

@st.cache_data()
def draw(prompt):
    client = OpenAI(api_key=apikey)
    response = client.images.generate(model="dall-e-3", prompt=f'{prompt}와 관련된 음식 메뉴 하나를 그려줘')
    image_url = response.data[0].url
    image = f"![alt text]({image_url})"
    return image

if st.button("start"):
    img = draw(prompti)
    st.markdown(img)
