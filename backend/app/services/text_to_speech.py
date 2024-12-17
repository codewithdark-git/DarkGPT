import openai

def handle_audio_upload(file):
    # Process the audio file and convert to text using OpenAI Whisper
    audio_content = file.read()
    response = openai.Audio.transcribe("whisper-1", audio_content)
    return response['text']
