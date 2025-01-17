import re
from constants import *
from ImageGenerator import StabilityImageGenerator
from ContentSpecs import VideoSpec
from utils import encode_png_to_base64
import os
import uuid
from typing import Generator
from NarrationGenerator import generate_narration_audio
from moviepy.editor import (
    ImageClip, TextClip, CompositeVideoClip, AudioFileClip, concatenate_videoclips, vfx
)


def parse_narration_and_captions(text: str) -> tuple[list[str], list[str]]:
    """
    Given a string that contains narration and image captions (delimited by %^ ... %^),
    return two lists:
      1) A list of narration segments (excluding content within %^ markers).
      2) A list of caption segments (the text found within %^ markers).

    :param text: The full raw text containing narration and %^ ... %^ caption blocks.
    :return: A tuple of two lists: (narration_list, caption_list).
    """

    # Regex to match all blocks between %^ ... %^ (including multiline).
    # We capture the text in a group so we can extract it as captions.
    pattern = r'%\^(.*?)%\^'  # Use parentheses to capture the content inside

    # 1. Find all caption blocks (the group inside %^...%^).
    captions = re.findall(pattern, text, flags=re.DOTALL)

    # 2. Remove the caption blocks from the original text, leaving only narration.
    #    We'll replace them with an empty string.
    narration_removed = re.sub(pattern, '', text, flags=re.DOTALL)

    # 3. Split narration into lines, stripping whitespace, keeping non-empty lines.
    narration_lines = [line.strip() for line in narration_removed.split('\n') if line.strip()]

    # 4. Similarly, split each caption into lines if desired, or keep them as raw blocks.
    #    For consistency, let's split them line-by-line as well and flatten or keep them separate.
    #    If you want each entire block as one entry, skip splitting by lines and just strip() them.
    caption_list = []
    for cap in captions:
        # Split by newline, remove blank lines
        lines = [line.strip() for line in cap.split('\n') if line.strip()]
        # If you prefer each entire caption block as one string, replace these 2 lines with:
        # lines = [cap.strip()]
        caption_list.extend(lines)

    return narration_lines, caption_list

class VideoGenerator:

    def __init__(self, script : str, video_spec : VideoSpec):
        self.script = script
        self.video_spec = video_spec
    
    def generate_video(self) -> str: #type: ignore
        pass

    def generate_image(self, prompt : str, image : str | None = None) -> str:
        """Given an image prompt generates the image and returns filepath 

        Args:
            prompt (str): prompt for image generation model
            image (str): base64 encoded file of the image

        Returns:
            str: filepath of generated image
        """
        caption = "Make the following image description in {} style: {}".format(self.video_spec.visual_art_style, prompt)
        if self.video_spec.image_model_name and self.video_spec.image_model_name.split("-")[0] == "stability":
            image_path = StabilityImageGenerator().generate_image(caption, self.video_spec.get_aspect_ratio(),self.video_spec.image_model_name, self.video_spec.visual_art_style, image = image)
        else:
            raise Exception("Unsupported model selected in video spec.")
        return image_path


class MontageGenerator(VideoGenerator):

    def __init__(self, script : str, video_spec : VideoSpec):
        super().__init__(script, video_spec)
        self.narrations, self.image_prompts = parse_narration_and_captions(script)
        assert len(self.narrations) == len (self.image_prompts)
        self.image_filepaths = []
        self.narration_filepaths = []

    def generate_video(self) -> str: 
        i = 0
        assert len(self.image_filepaths) == len(self.image_prompts)
        for image_filepath in self.image_filepaths:
            narration = self.narrations[i]
            narration_filepath = self.narration_filepaths[i]
            clip = self.generate_montage_clip(image_filepath, narration_filepath, narration)
            i+=1
            break

        return ""
    
    def generate_montage_clip(self, image_path: str, narration_path: str, narration_text: str) -> str:
        """
        Given an image filepath and narration audio file, generates a video
        whose length matches the narration audio. The video displays the image
        with a slow Ken Burns zoom effect and overlays the narration text as a caption.
        
        Args:
            image_path (str): Path to an image file (e.g., 'myphoto.jpg').
            narration_path (str): Path to an MP3 (or other audio) file containing narration.
            narration_text (str): A string of text to overlay as a caption.

        Returns:
            str: The filepath to the completed clip (e.g., 'montage_<uuid>.mp4').
        """

        # 1) Load the narration audio to determine clip duration
        audio_clip = AudioFileClip(narration_path)
        clip_duration = audio_clip.duration

        # 2) Create an ImageClip from the image, with the same duration
        base_clip = ImageClip(image_path).set_duration(clip_duration)

        final_clip = CompositeVideoClip([base_clip])

        # 6) Set the audio track to the narration audio
        #    (replace any existing audio with your narration)
        final_clip = final_clip.set_audio(audio_clip)

        # 7) Write out the final MP4
        output_filename = f"{CLIPS_FILEPATH}_{uuid.uuid4()}.mp4"
        final_clip.write_videofile(
            output_filename,
            fps=24,
            codec="libx264",
            audio_codec="aac"
        )

        # Clean up to release resources
        final_clip.close()
        base_clip.close()
        base_clip.close()
        audio_clip.close()

        return output_filename

    def generate_narrations(self):
        """Generates narrations for each clip
        """
        out = []
        for narration in self.narrations:
            narration_filepath = generate_narration_audio(narration)
            out.append(narration_filepath)
        self.set_narration_filepaths(out)

    def generate_images(self):
        """Generates images for each image caption
        """
        out = []
        image = None
        for prompt in self.image_prompts:
            if image:
                image = self.generate_image(prompt, image)
                out.append(image)
            else:
                image = self.generate_image(prompt)
                out.append(image)
        self.set_image_filepaths(out)
    
    def set_narration_filepaths(self, narration_filepaths : list[str]):
        self.narration_filepaths = narration_filepaths

    def set_image_filepaths(self, image_filepaths : list[str]):
        self.image_filepaths = image_filepaths


if __name__ == "__main__":
    pass
        