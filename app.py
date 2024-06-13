import streamlit as st
from openai import OpenAI
import requests
from bs4 import BeautifulSoup

def draw(prompt):
    response = client.images.generate(model="dall-e-3", prompt=prompt)
    image_url = response.data[0].url
    image = f"![alt text]({image_url})"
    return image

apikey = st.text_input("api key를 입력하세요", type="password")

if apikey:
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

    def download_and_save(url, filename):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        with open(filename, 'w') as fo:
            fo.write(text)

    url1 = "https://www.diningcode.com/list.dc?query=%EA%B2%BD%EC%84%B1%EB%8C%80%EB%B6%80%EA%B2%BD%EB%8C%80&order=r_score" # 광안대교
    filename1 = 'diamond_bridge.txt'
    download_and_save(url1, filename1)

    url2 = "https://ko.wikipedia.org/wiki/%EB%B6%80%EC%82%B0%EA%B4%91%EC%97%AD%EC%8B%9C" # 부산광역시
    filename2 = 'busan.txt'
    download_and_save(url2, filename2)

    with open(filename2) as fi:
        text = fi.read()

    vector_store = client.beta.vector_stores.create(name="BUSAN")

    file_paths = [filename1, filename2]
    file_streams = [open(path, "rb") for path in file_paths]

    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id,
        files=file_streams
    )

    if st.button("start assistant"):
        assistant = client.beta.assistants.create(
            instructions="당신은 부경대 맞집 추천가입니다. 첨부 파일의 정보를 이용해 응답하세요.",
            model="gpt-4-turbo-preview",
            tools=[{"type": "file_search"}],
            tool_resources={
                "file_search": {
                    "vector_store_ids": [vector_store.id]
                }
            }
        )

        thread = client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": "맛집 추천",
                }
            ]
        )

        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant.id
        )

        thread_messages = client.beta.threads.messages.list(thread.id, run_id=run.id)

        for msg in thread_messages.data:
            st.write(f"{msg.role}: {msg.content[0].text.value}")
