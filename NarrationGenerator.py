
from openai import OpenAI
from dotenv import load_dotenv
import uuid
from constants import *
load_dotenv()


def calculate_narration_cost(narration : str) -> float:
    num_chars = len(narration)
    #cost per 1m characters https://platform.openai.com/docs/pricing
    cost_per_1m = 15.0

    return num_chars * cost_per_1m / (10**6)


def generate_narration_audio(narration : str) -> tuple[str, float]:
    cost = 0
    output_path = NARRATION_FILEPATH + "/" + str(uuid.uuid4()) + ".mp3"
    client = OpenAI()
    response = client.audio.speech.create(
        model="tts-1",
        voice="echo",
        input=narration,
    )
    response.stream_to_file(output_path)
    return output_path, calculate_narration_cost(narration)