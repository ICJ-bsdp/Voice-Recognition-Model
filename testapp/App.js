import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';

export default function App() {

  useEffect(() => {
    var sdk = require("microsoft-cognitiveservices-speech-sdk");
    var fs = require("fs");

    // Replace with your own subscription key, service region (e.g., "westus"), and
    // the name of the file you want to run through the speech recognizer.
    var subscriptionKey = "YourSubscriptionKey";
    var serviceRegion = "YourServiceRegion"; // e.g., "westus"
    var filename = "YourAudioFile.wav"; // 16000 Hz, Mono

    // Create the push stream we need for the speech sdk.
    var pushStream = sdk.AudioInputStream.createPushStream();

    // Open the file and push it to the push stream.
    fs.createReadStream(filename).on('data', function(arrayBuffer) {
      pushStream.write(arrayBuffer.buffer);
    }).on('end', function() {
      pushStream.close();
    });

    // We are done with the setup
    console.log("Now recognizing from: " + filename);

    // Create the audio-config pointing to our stream and
    // the speech config specifying the language.
    var audioConfig = sdk.AudioConfig.fromStreamInput(pushStream);
    var speechConfig = sdk.SpeechConfig.fromSubscription(subscriptionKey, serviceRegion);

    // Setting the recognition language to English.
    speechConfig.speechRecognitionLanguage = "en-US";

    // Create the speech recognizer.
    var recognizer = new sdk.SpeechRecognizer(speechConfig, audioConfig);

    // Start the recognizer and wait for a result.
    recognizer.recognizeOnceAsync(
      function (result) {
        console.log(result);

        recognizer.close();
        recognizer = undefined;
      },
      function (err) {
        console.trace("err - " + err);

        recognizer.close();
        recognizer = undefined;
      });
  
    return () => {
    }
  }, [])
  
  return (
    <View style={styles.container}>
      <Text>Open up App.js to start working on your app!</Text>
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
