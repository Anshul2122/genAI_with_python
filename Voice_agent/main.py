from dotenv import load_dotenv
import os
import speech_recognition as sr
from openai import OpenAI
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer
import asyncio
from gtts import gTTS
import pygame
import io

load_dotenv()

async_client = AsyncOpenAI()

async def tts(speech:str):
    # async with async_client.audio.speech.create(
    #     model="tts-1",
    #     voice="alloy",
    #     input=speech,
    #     instructions="""Speak in a clear and concise manner,
    #     suitable for a voice assistant responding to user queries.""",
    #     response_format="pcm"
    # ) as response:
    #     await LocalAudioPlayer.play(response)
    
    tts = gTTS(text=speech, lang='en')
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_fp, "mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)




client = OpenAI(
    
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


def main():
    
    SYSTEM_PROMPT = """You are a expert voice agent. You are given
    the transcript of what user has said using voice.
    You need to output as if you are an voice agent and whatever you speak
    will be converted back to audio using text audio using AI and played back to user.
    So you need to be concise and clear in your response."""
    
    r = sr.Recognizer()
    
    with sr.Microphone(device_index=2) as source:
        print("Starting... adjusting for noise...")
        r.adjust_for_ambient_noise(source, duration=2)
        r.pause_threshold = 2
        
        messages= [
            {"role": "system", "content": SYSTEM_PROMPT},
        ]
        
        while True:
        
        
            try:
                print("Listening...")
                audio = r.listen(source,timeout=5, phrase_time_limit=10)
                print("processing... audio...")
                stt = r.recognize_google(audio)
                print("you said: ", stt)
            except sr.WaitTimeoutError:
                print("No speech detected.")
                return
            except sr.UnknownValueError:
                print("Could not understand audio — please speak clearly and try again.")
                return
            except sr.RequestError as e:
                print(f"Could not reach Google Speech API: {e}")
                return
            
            messages.append({"role": "user", "content": stt})
                
            response = client.chat.completions.create(
                model="gemini-2.5-flash",
                messages=[messages]
            )
            
            reply = response.choices[0].message.content
            print("Response:", reply)
            tts(reply)
        
        
main()