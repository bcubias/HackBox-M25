import streamlit as st
from pipeline.chatmodel import chat_with_gpt4o
from pipeline.mainpipeline import optimizted_prompt
from tts import text_to_speech
import azure.cognitiveservices.speech as speechsdk

key = st.secrets.Azurekey
endpoint = st.secrets.Azureendpoint
region = st.secrets.speech_region

def page_config(page_id):
    st.title(page_id)

    col1, col2 = st.columns([5, 2])

    speech_to_text = st.button("Speech to Text", disabled=st.session_state.running)
  
    # User Input
    if prompt := st.chat_input("Enter your message:", max_chars=4096, on_submit=disable()):
        respond(prompt, page_id)
            
    if speech_to_text:
        speech = recognize_microphone(key, region)
        if speech:
            respond(speech, page_id)
        
    # Display Messages & Logs
    with col1.container(height=525, border=False):
        for i, message in enumerate(st.session_state.pages[page_id][0]):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                st.button("", icon=":material/text_to_speech:", key=f"chat_{page_id}_{i}", type="tertiary",  
                    on_click=text_to_speech, args=(message["content"],), help="Text to Speech")
                
    with col2.container(height=525, border=False):
        for i, log in enumerate(st.session_state.pages[page_id][1]):
            with st.chat_message("ai"):
                st.markdown(log)
                st.button("", icon=":material/text_to_speech:", key=f"log_{page_id}_{i}", type="tertiary",  
                        on_click=text_to_speech, args=(log,), help="Text to Speech")


def disable():
    st.session_state.running = True
    
def respond(prompt, page_id):
    # Optimize Prompt
    optimized = optimizted_prompt(prompt)

    # Save log
    st.session_state.pages[page_id][1].append(optimized["log"])
    st.session_state.pages[page_id][0].append({"role": "user", "content": optimized["prompt"]})

    response = chat_with_gpt4o(optimized["prompt"], optimized["warning"])
    st.session_state.pages[page_id][0].append({"role": "assistant", "content": response})

    st.session_state.running = False
    st.rerun()
    
def recognize_microphone(key, region, language = "en-US"):
    # Create a speech configuration object
    speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
    speech_config.speech_recognition_language = language

    # Create a recognizer with the given settings
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # Start recognition and wait for a result
    result = recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        st.error("No speech could be recognized")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        st.error(f"Speech Recognition canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            st.error(f"Error details: {cancellation_details.error_details}")
    