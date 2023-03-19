import os
import azure.cognitiveservices.speech as speechsdk
import time

def recognize_from_microphone():
    speech_translation_config = speechsdk.translation.SpeechTranslationConfig(subscription='6c1f18d17acb4e4d84c4dc228d560c3b', region='eastus')
    speech_translation_config.speech_recognition_language="en-US"
    speech_translation_config.set_profanity(speechsdk.ProfanityOption.Raw)
    #speech_translation_config.set_property(property_id = speechsdk.PropertyId.SpeechServiceResponse_StablePartialResultThreshold, value = 5)

    target_language="es" # main spoken language : this language will display on OLED display
    speech_translation_config.add_target_language(target_language)

    auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(languages=["en-US", "zh-CN", "ja-JP", "es-ES"])

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    translation_recognizer = speechsdk.translation.TranslationRecognizer(translation_config=speech_translation_config, audio_config=audio_config, auto_detect_source_language_config=auto_detect_source_language_config)
    
    def result_callback(event_type: str, evt: speechsdk.translation.TranslationRecognitionEventArgs):
        """callback to display a translation result"""
        print("{}:\n {}\n\tTranslations: {}\n\tResult Json: {}\n".format(
            event_type, evt, evt.result.translations.items(), evt.result.json))

    done = False

    def stop_cb(evt: speechsdk.SessionEventArgs):
        """callback that signals to stop continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        nonlocal done
        done = True

    def canceled_cb(evt: speechsdk.translation.TranslationRecognitionCanceledEventArgs):
        print('CANCELED:\n\tReason:{}\n'.format(evt.result.reason))
        print('\tDetails: {} ({})'.format(evt, evt.result.cancellation_details.error_details))
    
    # connect callback functions to the events fired by the translation_recognizer
    translation_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    translation_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    # event for intermediate results
    translation_recognizer.recognizing.connect(lambda evt: result_callback('RECOGNIZING', evt))
    # event for final result
    translation_recognizer.recognized.connect(lambda evt: result_callback('RECOGNIZED', evt))
    # cancellation event
    translation_recognizer.canceled.connect(canceled_cb)

    # stop continuous recognition on either session stopped or canceled events
    translation_recognizer.session_stopped.connect(stop_cb)
    translation_recognizer.canceled.connect(stop_cb)

    def synthesis_callback(evt: speechsdk.translation.TranslationRecognitionEventArgs):
        """
        callback for the synthesis event
        """
        print('SYNTHESIZING {}\n\treceived {} bytes of audio. Reason: {}'.format(
            evt, len(evt.result.audio), evt.result.reason))

    # connect callback to the synthesis event
    translation_recognizer.synthesizing.connect(synthesis_callback)

    # start translation
    translation_recognizer.start_continuous_recognition()

    while not done:
        time.sleep(.5)

    translation_recognizer.stop_continuous_recognition()

recognize_from_microphone()