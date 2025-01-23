from data_collectors.Wikipedia import Wikipedia
from ContentSpecs import VideoSpec
from ScriptGenerator import MontageScriptGenerator
from VideoGenerator import MontageGenerator
from utils import *
from constants import *

# Inputs
text_name = "park chung hee"
wikipedia_url = "https://en.wikipedia.org/wiki/Assassination_of_Park_Chung_Hee"

type = CONTENT_TYPES.montage
tone = CONTENT_TONES.historian
output_format = OUTPUT_FORMATS.tiktok
duration = 5
image_model_name = IMAGE_MODEL_NAMES.stability_core
visual_art_style =VISUAL_ART_STYLES.comic_book
background_music = BACKGROUND_MUSIC.kobe 
script_gen_model = TEXT_MODEL_NAMES.openai_4o

# End of Inputs

raw_text_location = f"text_data/{text_name}"
script_location = f"text_data/{text_name} script.json"
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

script_generator = MontageScriptGenerator(text, video_spec, model_name=script_gen_model.value)

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

video_filepath, cost = video_gen.generate_video()

cost_summary["transcription_model"] = round(cost, 5)

cost_summary["total_cost"] = round(sum(cost_summary[key] for key in cost_summary.keys()),5)

print(video_filepath)
print(cost_summary)








