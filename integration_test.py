from data_collectors.Wikipedia import Wikipedia
from ContentSpecs import VideoSpec
from ScriptGenerator import MontageScriptGenerator
from VideoGenerator import MontageGenerator
from utils import save_string_as_text, load_string_from_text, calculate_model_cost
from constants import *

raw_text_location = "text_data/raw_text"
script_location = "text_data/siege of yorktown script"

wikipedia = Wikipedia(url="https://en.wikipedia.org/wiki/Siege_of_Yorktown")

# Source data gathering

# text = wikipedia.get_text()

# save_string_as_text(raw_text_location, text)

# text = load_string_from_text(raw_text_location)

# Script Generation

query = "Create a script for an entertaining historical video describing this"
type = CONTENT_TYPES.montage
tone = CONTENT_TONES.historian
output_format = OUTPUT_FORMATS.youtube
duration = 5
image_model_name = IMAGE_MODEL_NAMES.stability_core
visual_art_style =VISUAL_ART_STYLES.comic_book

print(visual_art_style)

video_spec = VideoSpec(type, tone, output_format, duration, visual_art_style, image_model_name)

# script_generator = MontageScriptGenerator(text, query, video_spec, model_name="gpt-4o-mini")

# response = script_generator.generate_script()

# save_string_as_text(script_location, response["script"])

# output_cost = calculate_model_cost(response["prompt_tokens"], response["completion_tokens"], response["model_name"])

# Video assembly

script = load_string_from_text(script_location)

video_gen = MontageGenerator(script, video_spec)

video_gen.generate_video()


