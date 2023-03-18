import os
import azure.cognitiveservices.speech as speechsdk
import time

def recognize_from_microphone():
    speech_config = speechsdk.SpeechConfig(subscription=('ca5c981b5b02433883bcb941aecb7e03'), region=('eastus'))
    speech_config.speech_recognition_language="zh-CN" #en-US  zh-CN es-ES
    speech_config.set_profanity(speechsdk.ProfanityOption.Raw)

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    
    print("Speak into your microphone.")
    
    # for i in range(10):
    #     time.sleep(0.5)
    #     speech_recognition_result = speech_recognizer.().get()
    #     print("Recognized: {}".format(speech_recognition_result.text))

    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")

recognize_from_microphone()