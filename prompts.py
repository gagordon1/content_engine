

TONE_MAP = {
      "historian" : "\nYou are a Harvard educated historian"
}

MONTAGE_NARRATION_FORMAT_PROMPT = """
{source_data}
{tone_prompt}
please summarize the content as a narration in a format suitable for a {duration} minute {output_format} narrated video.
Take the most entertaining / engaging moments of the content to keep the audience engaged.
Each sentence in the narration should have an associated image prompt that will prompt different image generation models to accompany the voiceover with images.
Each image prompt will be used to prompt an image generation model, so all necessary context to maintain continuity in the video should be present. [IMPORTANT] assume each image prompt is submitted independently of the others to a different artist. make sure all necessary details around time period / setting are captured in the image prompt

Please format your response as a valid json object with two fields "image_prompts" and "narrations" which map to lists of text.
So each narration should have exactly one associated image prompt. 
[IMPORTANT] Do not include any characters outside of the json object in the response. [IMPORTANT] (i.e. "```json" MUST not be in the response!)
For example:

    "image_prompts" : [
        "A north american brown fox jumping over a pine tree"
    ],
    "narrations" : [
        "The fox jumped over the tree."
    ]

"""