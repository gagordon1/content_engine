
IMAGE_FILEPATH = "temp_images/"

ASPECT_RATIOS = {
    "youtube" : "16:9"
}

#Company name a prefix to model name separated by "-"
IMAGE_MODEL_NAMES = {"stability-ultra", "stability-core"}

VISUAL_ART_STYLES = {"3d-model", "analog-film", "anime", "cinematic", "comic-book", "digital-art", 
                     "enhance", "fantasy-art", "isometric", "line-art", "low-poly", "modeling-compound", 
                     "neon-punk", "origami", "photographic", "pixel-art", "tile-texture"}

VALID_CONTENT_TYPES = {"slideshow", "montage", "promotional", "tutorial"}
VALID_CONTENT_TONES = {"formal", "informal", "dramatic", "friendly", "historian"}
VALID_OUTPUT_FORMATS = {"youtube", "tiktok"}

DEFAULT_IMAGE_FORMAT = "png"

# https://platform.openai.com/docs/pricing
OPENAI_PRICING_MAP = {
    "gpt-4o-mini" : {
        "input" : .15,
        "output" : .6
    },
    "gpt-4o": {
        "input" : 2.5,
        "output" : 10
    }
}

#https://platform.stability.ai/docs/api-reference#tag/Generate/paths/~1v2beta~1stable-image~1generate~1sd3/post
#credits per generation, 1 credit = $0.01
STABILITY_PRICING_MAP = {
    "core" : 3,
    "ultra" : 8,
    "sd3.5-large": 6.5,
    "sd3.5-large-turbo" : 4,
    "sd3-medium" : 3.5
}