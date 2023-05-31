import streamlit as st
import requests
import dotenv
import os
dotenv.load_dotenv('.env')

url = "https://play.ht/api/v1/convert"


payload = {
    "content": ["Hello everyone. I am grateful today for all the blessings in my life."],
    "voice": "en-US-JennyNeural",
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "AUTHORIZATION": os.getenv('SECRET_KEY'),
    "X-USER-ID": os.getenv('USER_ID')
}

response = requests.post(url, json=payload, headers=headers)
#st.write(" Response from post method: ")
#st.write(response.text)

response_data = response.json()
transcription_id = response_data.get('transcriptionId')
st.write(" transcriptionId: ")
st.write(transcription_id)
url = "https://play.ht/api/v1/articleStatus?transcriptionId={}".format(transcription_id)

headers = {
    "accept": "application/json",
    "AUTHORIZATION": os.getenv('SECRET_KEY'),
    "X-USER-ID": os.getenv('USER_ID')
}

response = requests.get(url, headers=headers)
while response.json()["converted"]== False:
    response = requests.get(url, headers=headers)
response_data = response.json()
audio_url = response_data.get('audioUrl')
st.write("**Click on the below URL to download the audio in mp3 format:**")
st.write(audio_url)
