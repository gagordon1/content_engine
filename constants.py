from enum import Enum


IMAGE_FILEPATH = "temp_images/"

CLIPS_FILEPATH = "temp_clips/"

NARRATION_FILEPATH = "temp_narrations/"

COMPLETED_VIDEO_FILEPATH = "completed_videos/"

BACKGROUND_MUSIC_FILEPATH = "background_music/"

TEMP_AUDIO_FILEPATH = "temp_audio/"

ASPECT_RATIOS = {
    "youtube" : "16:9",
    "tiktok" : "9:16"
}



#Company name a prefix to model name separated by "-"
class IMAGE_MODEL_NAMES(str, Enum):
    stability_ultra = "stability-ultra" 
    stability_core = "stability-core"

class VISUAL_ART_STYLES(str, Enum): 
    model_3d = "3d-model"
    analog_film = "analog-film"
    anime = "anime"
    cinematic = "cinematic"
    comic_book = "comic-book"
    digital_art = "digital-art"
    enhance = "enhance"
    fantasy_art = "fantasy-art"
    isometric = "isometric"
    line_art = "line-art"
    low_poly = "low-poly"
    modeling_compound = "modeling-compound"
    neon_punk = "neon-punk"
    origami = "origami"
    photographic = "photographic"
    pixel_art = "pixel-art"
    tile_texture = "tile-texture"

class CONTENT_TYPES(str, Enum): 
    slideshow = "slideshow"
    montage = "montage"
    promotional = "promotional"
    tutorial = "tutorial"

class CONTENT_TONES(str, Enum):
    formal = "formal"
    informal = "informal"
    dramatic = "dramatic"
    friendly = "friendly"
    historian = "historian"

class BACKGROUND_MUSIC(str, Enum):
    kobe = "kobe.mp3"

class TEXT_MODEL_NAMES(str, Enum):
    openai_4o_mini = "gpt-4o-mini"
    openai_4o = "gpt-4o"
    openai_o1 = "o1"
    openai_o1_mini = "o1-mini"

# VALID_OUTPUT_FORMATS = {"youtube", "tiktok"}

class OUTPUT_FORMATS(str, Enum):
    youtube = "youtube"
    tiktok = "tiktok"

DEFAULT_IMAGE_FORMAT = "png"

# https://platform.openai.com/docs/pricing
OPENAI_PRICING_MAP : dict[str, dict[str, float]] = {
    "gpt-4o-mini" : {
        "input" : .15,
        "output" : 0.6
    },
    "gpt-4o": {
        "input" : 2.5,
        "output" : 10.0
    },
    "o1" : {
        "input" : 15.0,
        "ouput" : 60.0
    },
    "o1-mini" : {
        "input" : 3.0,
        "output" : 12.0
    },
    "whisper-1" : {
        "input" : 0.0006
    }
}

#https://platform.stability.ai/docs/api-reference#tag/Generate/paths/~1v2beta~1stable-image~1generate~1sd3/post
#credits per generation, 1 credit = $0.01
STABILITY_PRICING_MAP : dict[str, float] = {
    "core" : 3.0,
    "ultra" : 8.0,
    "sd3.5-large": 6.5,
    "sd3.5-large-turbo" : 4.0,
    "sd3-medium" : 3.5
}

IMAGE_SCRIPT_SEPARATOR = "@"