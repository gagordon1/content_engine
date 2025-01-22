# add_captions.py

from typing import List
from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip, ColorClip
from typing import TypedDict
from PIL import ImageFont, ImageDraw, Image
import os
import json
from utils import load_list_from_json  # Ensure this function correctly loads the JSON list


class TranscriptionWord(TypedDict):
    start: float
    end: float
    word: str


def load_transcription_words(json_path: str) -> List[TranscriptionWord]:
    """Load transcription words from a JSON file."""
    if not os.path.isfile(json_path):
        raise FileNotFoundError(f"JSON file not found: {json_path}")
    
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Validate data format
    if not isinstance(data, list):
        raise ValueError("JSON data must be a list of transcription words.")
    
    for item in data:
        if not all(k in item for k in ("start", "end", "word")):
            raise ValueError("Each transcription word must have 'start', 'end', and 'word' fields.")
    
    return data


def measure_text(text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    """Measure the width and height of the given text using PIL."""
    # Create a sufficiently large image
    im = Image.new(mode="RGB", size=(1000, 1000))
    draw = ImageDraw.Draw(im)
    # Calculate text bounding box
    bbox = draw.textbbox((0, 0), text=text, font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    return width, height


def add_captions_helper(
    transcription_words: List[TranscriptionWord],
    video: VideoFileClip | CompositeVideoClip,
    font_path: str = "fonts/MechanicalBold-oOmA.otf",
    font_size: int = 70,
    font_color: str = "white",
    stroke_color: str = "black",
    stroke_width: int = 2,
    margin_bottom: int = 100,
    background_color: tuple = (0, 0, 0),
    background_opacity: float = 0.6,
    padding: int = 10,
) -> CompositeVideoClip:
    """
    Adds captions to the video file clip recursively. Each line contains as many words as fit,
    with words appearing one at a time from left to right.
    
    Args:
        transcription_words (List[TranscriptionWord]): List of transcribed words.
        video (VideoFileClip): The input video.
        font_path (str): Path to the font file.
        font_size (int): Font size.
        font_color (str): Text color.
        stroke_color (str): Text stroke color.
        stroke_width (int): Width of the text stroke.
        margin_bottom (int): Distance from the bottom of the video.
        background_color (tuple): RGB color for background box.
        background_opacity (float): Opacity of background box (0 to 1).
        padding (int): Padding around the text inside the background box.
        line_spacing (int): Spacing between lines.
    
    Returns:
        CompositeVideoClip: The final video with captions.
    """
    # Verify font path
    if not os.path.isfile(font_path):
        raise FileNotFoundError(f"Font file not found: {font_path}")
    
    # Load font using PIL for measurement
    pil_font = ImageFont.truetype(font_path, font_size)
    
    video_width, video_height = video.size
    
    caption_clips = []
    
    def process_lines(words: List[TranscriptionWord], current_line: int) -> None:
        """Recursive helper function to process captions line by line."""
        if not words:
            return
        
        # Determine how many words can fit on this line
        line_words = []
        total_width = 0
        
        for word_info in words:
            word = word_info['word']
            word_width, _ = measure_text(word, pil_font)
            # Check if adding this word exceeds the video width
            if total_width + word_width  + 2* padding > video_width:
                break
            line_words.append(word_info)
            total_width += word_width + 2* padding
        
        curr_width = padding
        # Create captions for each word in the line
        for word_info in line_words:
            word = word_info['word']
            start = word_info['start']
            end = word_info['end']
            duration = max([w["end"] for w in line_words]) - start
            
            if duration <= 0:
                continue
            
            # Measure text size
            text_width, text_height = measure_text(word, pil_font)
            
            # Define background size
            box_width = text_width + 2 * padding
            box_height = text_height + 2 * padding
            
            # Starting and ending x positions
            initial_x = 0
            # Create the semi-transparent background box
            box_clip = (
                ColorClip(size=(box_width, box_height), color=background_color)
                .set_opacity(background_opacity)
                .set_start(start)
                .set_duration(duration)
                .set_position(
                    (
                        initial_x + curr_width,
                        video_height - margin_bottom
                    )
                )
            )
            
            # Create the TextClip
            txt_clip = (
                TextClip(
                    txt=word,
                    fontsize=font_size,
                    font=font_path,
                    color=font_color,
                    stroke_color=stroke_color,
                    stroke_width=stroke_width,
                    method="label",
                )
                .set_start(start)
                .set_duration(duration)
                .set_position(
                    (
                        initial_x + curr_width,
                        video_height - margin_bottom
                    )
                )
            )

            curr_width += box_width
            
            # Append clips to the list
            caption_clips.extend([box_clip, txt_clip])
        
        # Recursively process remaining words
        remaining_words = words[len(line_words):]
        process_lines(remaining_words, current_line + 1)
    
    # Start processing from the first line
    process_lines(transcription_words, current_line=0)
    
    # Combine the original video with all caption clips
    composite = CompositeVideoClip([video, *caption_clips])
    
    return composite


if __name__ == "__main__":
    pass
    # # Load transcription words from JSON
    # transcription_words: List[TranscriptionWord] = load_list_from_json("transcription_words.json")
    
    # # Load the video file
    # video = VideoFileClip("test_video/_b1b7d791-3415-4ac3-8d56-3d614f1de174.mp4")
    
    # # Add captions
    # composite = add_captions_helper(
    #     transcription_words=transcription_words,
    #     video=video,
    #     font_path="fonts/MechanicalBold-oOmA.otf",  # Ensure this path is correct
    #     font_size=48,  # Larger font size
    #     font_color="white",
    #     stroke_color="black",
    #     stroke_width=2,
    #     margin_bottom=100,  # Increased margin
    #     background_color=(0, 0, 0),  # Black background
    #     background_opacity=0.6,  # Semi-transparent
    #     padding=10,  # Padding around text
    # )
    
    # # Save the final video with captions
    # from VideoGenerator import VideoGenerator

    # vgen = VideoGenerator(None, None)  #type: ignore
    # vgen.save_video_file(composite, "caption_test.mp4")
    
    # # Close video clips to free resources
    # video.close()
    # composite.close()
