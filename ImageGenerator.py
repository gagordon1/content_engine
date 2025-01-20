from dotenv import load_dotenv
from constants import *
import requests
import uuid
import os
from typing import TypedDict, Literal

class StabilityRequestData(TypedDict, total=False):
    """
    Represents the form data for a Stability AI request, where 'prompt' is required
    and all other fields are optional.
    """
    # Required field:
    prompt: str

    # Optional fields:
    mode: Literal["text-to-image", "image-to-image"]
    aspect_ratio: str
    negative_prompt: str
    # style_preset only for core model
    style_preset : VISUAL_ART_STYLES
    seed: int  # 0 <= seed <= 4294967294
    strength : float #0-1 strength of attached image
    output_format: OUTPUT_FORMATS
    # Additional fields like model, cfg_scale, style_preset, etc. can also be added
    # as NotRequired keys if needed.

class ImageGenerator:

    def __init__(self, test = False):
        self.test = test

    def generate_image(self, prompt : str, aspect_ratio : str,  model_name : IMAGE_MODEL_NAMES, style_preset : VISUAL_ART_STYLES, image : str | None = None,) -> tuple[str, float]:
        """Given a text prompt returns the link to ai rendering of the text

        Args:
            prompt (str): text prompt to create an image from
            aspect_ratio (str): 16:9 1:1 21:9 2:3 3:2 4:5 5:4 9:16 9:21
            model_name (str): valid model name,
            style_preset (str) : vailid style_preset
            image (str): starting point for the image (optional)
        
        Retrurns: tuple of the filepath to completed image and float of the cost in USD
        """
        raise NotImplementedError("Subclasses must implement this method")
    
class StabilityImageGenerator(ImageGenerator):
    def __init__(self, test = False) -> None:
        super().__init__(test)

    def get_stability_cost(self, model : str) -> float:
        credits = STABILITY_PRICING_MAP[model]
        return credits / 100

    def make_stability_request(self, data, files, model : str) -> tuple[str, float]:
        cost = 0.0
        response = requests.post(
            f"https://api.stability.ai/v2beta/stable-image/generate/" + model,
            headers={
                "authorization": "Bearer {}".format(os.getenv("STABILITY_API_KEY")),
                "accept": "image/*"
            },
            files=files,
            data=data,
         )
        output_file = IMAGE_FILEPATH + str(uuid.uuid4()) + ".png"
        if response.status_code == 200:
            cost = self.get_stability_cost(model)
            with open(output_file, 'wb') as file:
                file.write(response.content)
        else:
            raise Exception(str(response.json()))
        
        return output_file, cost

    def generate_image(self, prompt : str, aspect_ratio : str,  
                       model_name : IMAGE_MODEL_NAMES, 
                       style_preset : VISUAL_ART_STYLES, image : str | None = None,) -> tuple[str, float]:
        load_dotenv()
        model = model_name.split("-")[1]
        data = {
                "prompt": prompt,
                "output_format": "png",
                "aspect_ratio" : aspect_ratio,
                "output_format" : DEFAULT_IMAGE_FORMAT
        }
        if model_name == "stability-ultra" or model_name == "stability-core":
            if model_name == "stability-core":
                if style_preset:
                    data["style_preset"] = style_preset.value
            
            if model_name == "stability-ultra":
                if image:
                    data["strength"] = .9 #type: ignore
                if image:
                    with open(image, "rb") as f:
                        files = {
                            "image": (image, f, "image/png")
                        }
                        output_file, cost = self.make_stability_request(data, files,model)
            else:
                files = {"none": ''}
                output_file, cost = self.make_stability_request(data, files, model)
        else:
            raise Exception("Model {} unsupported".format(model_name))
        return output_file, cost

if __name__ == "__main__":
    # generator = OpenAIImageGenerator()
    # generator.generate_image("playboi carti")
    pass