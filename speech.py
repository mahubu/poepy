import pyttsx3

DEFAULT_SPEECH_RATE = 175

# Initialize speaking engine
engine = pyttsx3.init()
engine.setProperty('rate', DEFAULT_SPEECH_RATE)


def say(sentence):
    engine.say(str(sentence))
    engine.runAndWait()


if __name__ == '__main__':
    say("Hello world!");
    engine.stop()
