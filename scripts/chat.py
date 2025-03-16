import streamlit as st
from pipeline.mainpipeline import optimizted_prompt
import azure.cognitiveservices.speech as speechsdk

key = st.secrets.key
endpoint = st.secrets.endpoint
region = st.secrets.speech_region


def page_config(page_id):
    # Page layout
    st.title(page_id)

    col1, col2 = st.columns([5, 2])
    speech_to_text = st.button("Speech to Text")
    
    # Chat input 
    if prompt := st.chat_input("What is up?", max_chars=st.session_state.char_limit):
        # Log user input
        st.session_state.pages[page_id][0].append({"role": "user", "content": prompt})

        respond(prompt, page_id)
        
    if speech_to_text:
        speech = recognize_microphone(key, region)
        if speech:
            st.session_state.pages[page_id][0].append({"role": "user", "content": speech})
            respond(speech, page_id)

    # Display chat messages
    with col1: 
        for message in st.session_state.pages[page_id][0]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Display logs
    with col2:
        for log in st.session_state.pages[page_id][1]:
            st.chat_message("ai").write(log)
            st.markdown("---")
    
def respond(prompt, page_id):
    # Get and log response and change
    message = optimizted_prompt(prompt)
    response = message["prompt"]

    st.session_state.pages[page_id][1].append(message["log"])
    st.session_state.pages[page_id][0].append({"role": "ai", "content": response})
    
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
    