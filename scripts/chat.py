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
    if prompt := st.chat_input("Enter your message:", max_chars=st.session_state.char_limit):
        respond(prompt, page_id)
            
    if speech_to_text:
        speech = recognize_microphone(key, region)
        if speech:
            respond(speech, page_id)
        
    # Display Messages & Logs
    with col1:
        for message in st.session_state.pages[page_id][0]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    with col2:
        for log in st.session_state.pages[page_id][1]:
            st.chat_message("ai").write(log)
            st.markdown("---")
    
def respond(prompt, page_id):
      # Optimize Prompt
      optimized = optimizted_prompt(prompt)

      # Save optimized prompt and log
      log_text = f"Log: {optimized['log']}" if optimized.get("log") else ""
      prompt_text = f"Turns Into: {optimized["prompt"]}" if optimized.get("prompt") else ""

      st.session_state.pages[page_id][0].append({"role": "user", "content": optimized["prevPrompt"]})
      st.session_state.pages[page_id][1].append(
          "Previous Prompt:" + optimized["prevPrompt"] + "\n"\
          + prompt_text + "\n"\
          + log_text
          )

      # Check for harmful content 
      if optimized["harm"]:
          response = chat_with_gpt4o(optimized["prevPrompt"], "harm")
          st.session_state.pages[page_id][0].append({"role": "assistant", "content": response})
      elif optimized["vague"]:
          response = chat_with_gpt4o(optimized["prevPrompt"], "vague")
          st.session_state.pages[page_id][0].append({"role": "assistant", "content": response})
      else:
          response = chat_with_gpt4o(optimized["prompt"])
          st.session_state.pages[page_id][0].append({"role": "assistant", "content": response})
    
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
    