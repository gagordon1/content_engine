from openai import OpenAI
from dotenv import load_dotenv
from moviepy.editor import AudioFileClip
from constants import *
from typing import TypedDict

load_dotenv()
client = OpenAI()

class TranscriptionWord(TypedDict):
    start : float
    end : float
    word : str

def get_timestamped_transcriptions(path_to_audio_file : str)-> tuple[list[TranscriptionWord], float]:
    """Transcribes audio, getting timestamps of each word along with start and end seconds

    Args:
        path_to_audio_file (str): path to an mp3 file

    Raises:
        Exception: If error transcribing the audio

    Returns:
        tuple[list[TranscriptionWord], float]: Tuple containing list of each transcribed word along with the cost to generate the transcription.
    """
    model = "whisper-1"
    audio_file = open(path_to_audio_file, "rb")
    audio = AudioFileClip(path_to_audio_file)
    duration_in_seconds = audio.duration
    transcription = client.audio.transcriptions.create(
        file=audio_file,
        model=model,
        response_format="verbose_json",
        timestamp_granularities=["word"]
    )
    cost = duration_in_seconds * OPENAI_PRICING_MAP[model]["input"] / 60
    if transcription.words:
        out : list[TranscriptionWord] = [w.to_dict() for w in transcription.words] #type: ignore
        return out, cost
    else:
        raise Exception("Error transcribing video audio.")