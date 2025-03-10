import re
from constants import *
from ImageGenerator import StabilityImageGenerator
from ContentSpecs import VideoSpec
import uuid
from ScriptGenerator import MontageScriptFormat
from NarrationGenerator import generate_narration_audio
from transcribe import get_timestamped_transcriptions, TranscriptionWord
from utils import save_list_as_json
from moviepy.editor import (
    ImageClip, TextClip, CompositeVideoClip, AudioFileClip, concatenate_videoclips, vfx, CompositeAudioClip, VideoFileClip
)
from captions import add_captions_helper
import json



class VideoGenerator:

    def __init__(self, script : str, video_spec : VideoSpec):
        self.script = script
        self.video_spec = video_spec
    
    def generate_video(self, output_path : str | None = None) -> str: #type: ignore
        pass

    def generate_image(self, prompt : str, image : str | None = None) -> tuple[str, float]:
        """Given an image prompt generates the image and returns filepath 

        Args:
            prompt (str): prompt for image generation model
            image (str): base64 encoded file of the image

        Returns:
            str: filepath of generated image
            float: cost to generate image in USD
        """
        cost = 0
        prompt = "Make the following image description in {} style: {}. Do not include text in the image.".format(self.video_spec.visual_art_style, prompt)
        if self.video_spec.image_model_name and self.video_spec.image_model_name.split("-")[0] == "stability":
            image_path, cost = StabilityImageGenerator().generate_image(prompt, self.video_spec.get_aspect_ratio(),self.video_spec.image_model_name, self.video_spec.visual_art_style, image = image)
        else:
            raise Exception("Unsupported model selected in video spec.")
        return image_path, cost
    
    def add_background_music(self, video : CompositeVideoClip) -> CompositeVideoClip:
        """Given a video, adds background music according to this generator's video spec

        Args:
            video (CompositeVideoClip): a video 

        Returns:
            CompositeVideoClip: video with background music added if specified
        """
        total_duration = video.duration
        if self.video_spec.background_music:
            music_track = AudioFileClip("{}/{}".format(BACKGROUND_MUSIC_FILEPATH, self.video_spec.background_music.value)).set_duration(total_duration).volumex(.08)
            narration_track = video.audio
            vid_audio = CompositeAudioClip([music_track, narration_track])
            video = video.set_audio(vid_audio) #type: ignore
        return video
    
    def save_audio_of_video_file(self, video : CompositeVideoClip | VideoFileClip) -> str:

        output_filename = f"{TEMP_AUDIO_FILEPATH}_{uuid.uuid4()}.mp3"
        audio = video.audio
        if audio:
            audio.fps = 44100
            audio.write_audiofile(
                output_filename,
                codec='libmp3lame',
                bitrate="128k",
                verbose=False,
                logger=None
            )
        
        return output_filename
    
    def save_video_file(self, video : CompositeVideoClip, output_filename = None) -> str:
        if output_filename == None:
            output_filename = f"{COMPLETED_VIDEO_FILEPATH}_{uuid.uuid4()}.mp4"
        
        video.write_videofile(
            output_filename,
            fps=24,
            codec="libx264",
            audio_codec="aac",
            verbose=False,
            logger=None
        )
        return output_filename
    
    def add_captions(self, video : CompositeVideoClip | VideoFileClip) -> tuple[CompositeVideoClip, float]:
        """Given a video clip, add typewriter captions

        Returns:
            CompositeVideoClip: video clip
        """
        audio_filepath = self.save_audio_of_video_file(video)
        transcription_words, cost = get_timestamped_transcriptions(audio_filepath)
        return add_captions_helper(transcription_words, video), cost
    
    def compile_clips(self, clip_paths: list[str]) -> CompositeVideoClip:
        clips : list[VideoFileClip] = []
        
        current_start = 0
        for path in clip_paths:
            clip = VideoFileClip(path)
            clip = clip.set_start(current_start)
            current_start += clip.duration
            clips.append(clip)

        total_duration = sum(c.duration for c in clips)
        return CompositeVideoClip(clips).set_duration(total_duration)

class MontageGenerator(VideoGenerator):

    def __init__(self, script : str, video_spec : VideoSpec):
        super().__init__(script, video_spec)
        print(script)
        script_dict : MontageScriptFormat = json.loads(script)
        self.narrations, self.image_prompts = script_dict["narrations"], script_dict["image_prompts"]
        assert len(self.narrations) == len (self.image_prompts)
        self.image_filepaths = []
        self.narration_filepaths = []

    def generate_video(self, output_path : str | None = None) -> tuple[str, float]: 
        """Generates a video assuming narrations and images have already been generated

        Returns:
            str: filepath to the completed video
            float: cost to add captions to video
        """
        assert len(self.image_filepaths) == len(self.image_prompts)
        assert len(self.narration_filepaths) == len(self.image_filepaths)
        
        clip_paths = []
        for i, image_filepath in enumerate(self.image_filepaths):
            narration = self.narrations[i]
            narration_filepath = self.narration_filepaths[i]
            clip = self.generate_montage_clip(image_filepath, narration_filepath, narration)
            clip_paths.append(clip)
        video = self.compile_clips(clip_paths)

        print("adding captions...")
        video, cost = self.add_captions(video)

        # add background music if selected 
        if self.video_spec.background_music:
            print("adding background music...")
            video = self.add_background_music(video)
        
        return self.save_video_file(video, output_filename=output_path), cost

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
        self.save_video_file(final_clip, output_filename=output_filename)
        # Clean up to release resources
        final_clip.close()
        base_clip.close()
        base_clip.close()
        audio_clip.close()

        return output_filename

    def generate_narrations_from_script(self) -> float:
        """Generates narrations for each clip
        Returns:
            float of total cost of the narrations
        """
        out = []
        total_cost = 0.0
        for narration in self.narrations:
            narration_filepath, cost = generate_narration_audio(narration)
            out.append(narration_filepath)
            total_cost += cost
        self.set_narration_filepaths(out)
        return total_cost

    def generate_images_from_script(self) -> float:
        """Generates images for each image caption
        Returns:
            float: total cost of creating images
        """
        out = []
        image = None
        total_cost = 0.0
        for prompt in self.image_prompts:
            if image:
                image, cost = self.generate_image(prompt, image)
                total_cost += cost
                out.append(image)
            else:
                image, cost = self.generate_image(prompt)
                total_cost += cost
                out.append(image)
        self.set_image_filepaths(out)
        return total_cost
    
    def set_narration_filepaths(self, narration_filepaths : list[str]):
        self.narration_filepaths = narration_filepaths

    def set_image_filepaths(self, image_filepaths : list[str]):
        self.image_filepaths = image_filepaths


if __name__ == "__main__":
    # test_video_no_background_music = "test_video/_b1b7d791-3415-4ac3-8d56-3d614f1de174.mp4"
    # video_gen = VideoGenerator(None, None) #type: ignore
    # video = video_gen.add_captions(VideoFileClip(test_video_no_background_music))
    pass
    