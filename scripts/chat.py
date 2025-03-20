import streamlit as st
from pipeline.chatmodel import chat_with_gpt4o
from pipeline.mainpipeline import optimizted_prompt
import azure.cognitiveservices.speech as speechsdk

key = st.secrets.Azurekey
endpoint = st.secrets.Azureendpoint
region = st.secrets.speech_region

def page_config(page_id):
    st.title(page_id)

    col1, col2 = st.columns([5, 2])

    speech_to_text = st.button("Speech to Text")
  
    # User Input
    if prompt := st.chat_input("Enter your message:", max_chars=4096):
        respond(prompt, page_id)
            
    if speech_to_text:
        speech = recognize_microphone(key, region)
        if speech:
            respond(speech, page_id)
        
    # Display Messages & Logs
    with col1.container(height=525, border=False):
        for message in st.session_state.pages[page_id][0]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    with col2.container(height=525, border=False):
        for log in st.session_state.pages[page_id][1]:
            st.chat_message("ai").write(log)
            st.markdown("---")
    
def respond(prompt, page_id):
    with st.status("Optimizing prompt...", expanded=True) as status:
        st.write("Analyzing user input...")

        # Optimize Prompt
        optimized = optimizted_prompt(prompt)

        st.write("Generating optimized version...")

        # Save log
        st.session_state.pages[page_id][1].append(optimized["log"])
        st.write("Checking for harmful content...")

        # Check for harmful content 
        st.session_state.pages[page_id][0].append({"role": "user", "content": optimized["prompt"]})

        st.write("Generating AI response...")

        response = chat_with_gpt4o(optimized["prompt"], optimized["warning"])
        st.session_state.pages[page_id][0].append({"role": "assistant", "content": response})

        status.update(label="Response complete!", state="complete", expanded=False)
    
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
    