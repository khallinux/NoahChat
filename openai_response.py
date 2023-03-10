from gtts import gTTS
import subprocess

def text_to_speech(text):
    tts = gTTS(text=text, lang='en', tld='us')
    tts.save("response.mp3")
    tts.speed = 0.5
    subprocess.Popen(['mpg321', 'response.mp3'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
