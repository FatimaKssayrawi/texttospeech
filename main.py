import streamlit as st
import requests
import dotenv
import os
import openai
dotenv.load_dotenv('.env')

url = "https://play.ht/api/v1/convert"

# Streamlit app title and description
st.title("Youtube Video Script Generator")
video_title = st.text_input("Enter the video's title",placeholder = "Essential Tips for Successful Job Interviews, Quick and Easy Dinner Recipes for Busy Parents")
video_description = st.text_input("Enter the video's description",
                                  placeholder = "From preparation to body language, we'll guide you towards success and help you land your dream job")
search_term = st.text_input('Enter search term',placeholder = "job interview tips,how to succeed in interviews,interview preparation advice")
tone_voice = st.text_input('Enter tone of voice', placeholder = "Supportive, empowering, informative")
length = st.number_input('Enter number of words')

# original prompt that includes all user's inputs
prompt = f"I want you to act as a scriptwriter for a YouTube video titled {video_title}.\
            Your task is to write in an {tone_voice} tone. Consider the video’s description: {video_description},\
            and the following search terms: {search_term}. The script should be a maximum of {length} tokens. Please be concise with the number of tokens."

chat_response = ''
# Button to fetch the response
# if the button is pressed, the code will be executed
if st.button("**Click here to generate script and audio**"):
# Check if product_name and product_description are provided
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.Completion.create(
            engine='text-davinci-003',  # Specify the GPT-3.5 model variant
            prompt=prompt, # set the user input from the txt area
            max_tokens=600  # Specify the desired length of the generated response
        )
    # response variable holds the API response

    # Extract the generated response from the API
    # retrieve the first response from the generated responses
        chat_response = response.choices[0].text.strip()

    # Display the response in Streamlit
        #st.write(" Youtube Video Script: ")
        #st.write(prompt)
        #st.write(chat_response)
def remove_text_in_brackets(text):
    result = ""
    inside_brackets = False
    inside_parentheses = False

    for char in text:
        if char == "[":
            inside_brackets = True
            continue
        elif char == "]":
            inside_brackets = False
            continue
        elif char == "(":
             inside_parentheses = True
             continue
        elif char == ")":
            inside_parentheses = False
            continue

        if not inside_brackets and not inside_parentheses:
            result += char

    return result

cleaned_text = remove_text_in_brackets(chat_response)
#st.write("**Your Youtube Video Script:**")
#st.write(cleaned_text)

def remove_words(text, words):
    for word in words:
        text = text.replace(word + ":", "")
    return text


words_to_remove = ["Narrator", "Host", "Presenter","Emcee", "Commentator",
                    "Announcer","Voiceover", "artist", "Speaker", "Performer",
                    "Character", "Actor/Actress", "Protagonist", "Antagonist",
                    "Interviewee", "Interviewer", "Expert", "Guest", "Intro","SPEAKER",
                   "Introduction", "Outro", "Conclusion", "Summary", "Co-host",
                   "Lead","Sidekick","Panelist","Moderator","Participant", "Script"
                   "Demonstrator","Coach","Mentor","Consultant","Guide","Support",
                    "Facilitator","Educator","Influencer","Expertise"," Specialist",
                   "Trainer", "Youtuber","Content creator","Vlogger","Showcaser","Reviewer"]

cleaned_text1 = remove_words(cleaned_text, words_to_remove)
st.write("**Your Youtube Generated Script:**")
st.write(cleaned_text1)
payload = {
    "content": [cleaned_text1],
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
#st.write(" transcriptionId: ")
#st.write(transcription_id)
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
