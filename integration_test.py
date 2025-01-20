from data_collectors.Wikipedia import Wikipedia
from ContentSpecs import VideoSpec
from ScriptGenerator import MontageScriptGenerator
from VideoGenerator import MontageGenerator
from utils import *
from constants import *

# Inputs
text_name = "battle of waterloo"
wikipedia_url = "https://en.wikipedia.org/wiki/Battle_of_Waterloo"

query = "Create a script for an entertaining historical video describing this"
type = CONTENT_TYPES.montage
tone = CONTENT_TONES.historian
output_format = OUTPUT_FORMATS.youtube
duration = 10
image_model_name = IMAGE_MODEL_NAMES.stability_core
visual_art_style =VISUAL_ART_STYLES.comic_book
background_music = BACKGROUND_MUSIC.kobe
script_gen_model = TEXT_MODEL_NAMES.openai_o1_mini

# End of Inputs

raw_text_location = f"text_data/{text_name}"
script_location = f"text_data/{text_name} script"
image_filepaths_json = "test_images/image_paths.json"
narration_filepaths_json = "test_narrations/narration_paths.json"

wikipedia = Wikipedia(url=wikipedia_url)

# Source data gathering

print("scraping wikipedia page...")

# text = wikipedia.get_text()

# save_string_as_text(raw_text_location, text)

text = load_string_from_text(raw_text_location)

# Script Generation

cost_summary = {
    "image_model" : 0.0,
    "text_model" : 0.0,
    "narration_model" : 0.0
}

video_spec = VideoSpec(type, tone, output_format, duration, visual_art_style, image_model_name, background_music)

script_generator = MontageScriptGenerator(text, video_spec, model_name=script_gen_model.value)

print("generating a script...")

# response = script_generator.generate_script()

# cost_summary["text_model"] = round(response["cost"],5)

# Video assembly
# script = response["script"]

# save_string_as_text(script_location, script)

script = load_string_from_text(script_location)

video_gen = MontageGenerator(script, video_spec)

print("generating audio narrations...")

cost = video_gen.generate_narrations_from_script()

cost_summary["narration_model"] = round(cost, 5)

print("generating accompanying images...")

cost = video_gen.generate_images_from_script()

cost_summary["image_model"] = round(cost, 5)

print("compiling video...")

video_filepath = video_gen.generate_video()

print(video_filepath)
print(cost_summary)








