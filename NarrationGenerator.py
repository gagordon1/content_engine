from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import uuid
from constants import *
load_dotenv()


def generate_narration_audio(narration : str) -> str:
    output_path = NARRATION_FILEPATH + "/" + str(uuid.uuid4()) + ".mp3"
    client = OpenAI()
    response = client.audio.speech.create(
        model="tts-1",
        voice="echo",
        input=narration,
    )
    response.stream_to_file(output_path)
    return output_path