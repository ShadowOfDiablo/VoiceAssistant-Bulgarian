import openai
from gtts import gTTS
import subprocess
import speech_recognition as sr

# Set your OpenAI API key
openai.api_key = ''

# Initialize a recognizer
recognizer = sr.Recognizer()

# Initialize an empty conversation
conversation = []

# Start a conversation with a system message to set the language to Bulgarian
system_message = {"role": "system", "content": "Language: bg"}
conversation.append(system_message)

while True:
    # Listen for user's spoken input
    with sr.Microphone() as source:
        print("Говорете сега...")
        audio = recognizer.listen(source, timeout=5)
    
    try:
        # Recognize the spoken input in Bulgarian
        user_input = recognizer.recognize_google(audio, language="bg-BG")
        print("Вие казахте:", user_input)

        # Add the user's message to the conversation
        user_message = {"role": "user", "content": user_input}
        conversation.append(user_message)

        # Send the conversation to the API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation
        )

        # Get the assistant's response
        assistant_response = response.choices[0].message.content

        # Print and speak the assistant's response in Bulgarian
        print("Асистент:", assistant_response)
        tts = gTTS(assistant_response, lang="bg")
        tts.save("assistant_response.mp3")

        # Use a media player to play the generated speech
        subprocess.run(["mpg123", "assistant_response.mp3"])

    except sr.UnknownValueError:
        print("Не успях да разпозная гласа ви. Моля, опитайте отново.")
    except sr.RequestError as e:
        print(f"Грешка при изпращане на заявка към разпознаването на реч: {e}")
    
    # Optionally, you can add a condition to end the conversation based on user input.
    # For example, if the user says "край," you can break out of the loop.

# End of the conversation
print("Край на разговора.")
