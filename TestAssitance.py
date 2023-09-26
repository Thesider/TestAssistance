import assemblyai as aai
import speech_recognition as sr
import google.generativeai as palm
import pyttsx3
import yaml
# Read the API keys from a YAML file
with open('C:/Users/BAO KHANG/Desktop/Test/hello/keys.yaml', 'r') as f:
    api_keys = yaml.safe_load(f)

# Set your AssemblyAI API key
aai.settings.api_key = api_keys['assemblyai_key']

# Set your API key for the palm API
palm.configure(api_key=api_keys['palm_key'])


# List available models
models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name

# Initialize the recognizer
r = sr.Recognizer()


# Use the microphone as the audio source
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    print("Please ask your question:")
    audio = r.listen(source, timeout=5, phrase_time_limit=5)

# Convert the speech to text
question = r.recognize_google(audio)
# Set the personality prompt
personality_prompt = """You are to act as an artificial intelligence bot that is here to assist humans.  
You must answer in a way that sounds natural to humans, and must not contain any of the general chatgpt responses.  
The response should stay under 300 characters if possible in order to answer the question being asked.

If anything is unclear, asked the user for clarifying questions before responding back to their answer. 
Else, at the end of each response, you should follow-up with a clarifying question related to what the user asked in order to further along the conversation.
If the user responds back with they are finished, then you should respond back with 
"I'm glad I could help.
Have a wonderful rest of your day!"
Are you ready?"""

# Generate text based on the transcribed speech
completion = palm.generate_text(
    model=model,
    prompt=question,
    temperature=0,
    max_output_tokens=800,
)

# Print the generated text
print(completion.result)
# Initialize the TTS engine
engine = pyttsx3.init()
# Set the voice to a personalized TTS voice
voices = engine.getProperty('voices')
voice = voices[0]  # Select the first voice in the list
engine.setProperty('voice', voice.id)


# Convert the generated text to speech
engine.say(completion.result)

# Play the speech
engine.runAndWait()