from data_collectors.Wikipedia import Wikipedia
from ContentSpecs import VideoSpec
from ScriptGenerator import MontageScriptGenerator
from VideoGenerator import MontageGenerator
from Uploader import TikTokUploader
import uuid
from utils import *
from constants import *

# Inputs
text_name = "jonestown"
wikipedia_url = "https://en.wikipedia.org/wiki/Jonestown"
description = "jonestown"

type = CONTENT_TYPES.montage
tone = CONTENT_TONES.historian
output_format = OUTPUT_FORMATS.tiktok
duration = 2
image_model_name = IMAGE_MODEL_NAMES.stability_core
visual_art_style =VISUAL_ART_STYLES.comic_book
background_music = BACKGROUND_MUSIC.good_night_lofi
script_gen_model = TEXT_MODEL_NAMES.deepseek_v2
script_gen_model_company = TEXT_MODEL_COMPANY.deepseek

# End of Inputs

raw_text_location = f"{TEXT_DATA_PATH}/{text_name}"
script_location = f"{MONTAGE_SCRIPT_PATH}/{text_name} script.json"
image_filepaths_json = "test_images/image_paths.json"
narration_filepaths_json = "test_narrations/narration_paths.json"

wikipedia = Wikipedia(url=wikipedia_url)

# Source data gathering

print("scraping wikipedia page...")

text = wikipedia.get_text()

save_string_as_text(raw_text_location, text)

text = load_string_from_text(raw_text_location)

# Script Generation

cost_summary = {
    "image_model" : 0.0,
    "text_model" : 0.0,
    "narration_model" : 0.0,
    "transcription_model" : 0.0,
    "total_cost" : 0.0
}

video_spec = VideoSpec(type, tone, output_format, duration, visual_art_style, image_model_name, background_music)

script_generator = MontageScriptGenerator(text, video_spec, script_gen_model, script_gen_model_company)

print("generating a script...")

response = script_generator.generate_script()

cost_summary["text_model"] = round(response["cost"],5)

# # Video assembly
script = response["script"]

save_dict_as_json(script_location, script) #type: ignore

script = str(load_dict_from_json(script_location))

video_gen = MontageGenerator(script, video_spec) #type: ignore

print("generating audio narrations...")

cost = video_gen.generate_narrations_from_script()

cost_summary["narration_model"] = round(cost, 5)

print("generating accompanying images...")

cost = video_gen.generate_images_from_script()

cost_summary["image_model"] = round(cost, 5)

print("compiling video...")

completed_video_output_path = f"{COMPLETED_VIDEO_FILEPATH}{text_name}{str(uuid.uuid4())}.mp4"
video_filepath, cost = video_gen.generate_video(output_path = completed_video_output_path)

cost_summary["transcription_model"] = round(cost, 5)

cost_summary["total_cost"] = round(sum(cost_summary[key] for key in cost_summary.keys()),5)

t_upload = TikTokUploader()

print("uploading video to tiktok...")
t_upload.upload(video_filepath, description)

print(video_filepath)
print(cost_summary)








