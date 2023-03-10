from gtts import gTTS
import subprocess
import openai
from api_key import API_KEY
openai.api_key = API_KEY
def generate_openai_response(text_input):
    prompt = f" {text_input}"
    print("Prompt:", prompt)
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.3,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0.2,
        presence_penalty=0,
    )
    answer = response['choices'][0]['text']

    return answer

def text_to_speech(text):
    tts = gTTS(text=text, lang='en', tld='us')
    tts.save("response.mp3")
    tts.speed = 0.5
    subprocess.Popen(['mpg321', 'response.mp3'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
