import openai

def handle_video_upload(file):
    # Process the video file and convert to text using OpenAI Whisper
    video_content = file.read()
    response = openai.Audio.transcribe("whisper-1", video_content)
    return response['text']
