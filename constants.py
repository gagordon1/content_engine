from enum import Enum


IMAGE_FILEPATH = "temp_images/"

CLIPS_FILEPATH = "temp_clips/"

NARRATION_FILEPATH = "temp_narrations/"

COMPLETED_VIDEO_FILEPATH = "completed_videos/"

BACKGROUND_MUSIC_FILEPATH = "background_music/"

TEMP_AUDIO_FILEPATH = "temp_audio/"

TEXT_DATA_PATH = "text_data/"

MONTAGE_SCRIPT_PATH = "montage_scripts/"

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

class TEXT_MODEL_COMPANY(str, Enum):
    openai = "openai"
    deepseek = "deepseek"

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
    kobe = "kobe.mp3" #copyright issue
    good_night_lofi = "good-night-lofi-cozy-chill-music-160166.mp3"
    weeknds = "weeknds-122592.mp3"

class TEXT_MODEL_NAMES(str, Enum):
    openai_4o_mini = "gpt-4o-mini"
    openai_4o = "gpt-4o"
    openai_o1 = "o1-preview"
    openai_o1_mini = "o1-mini"
    deepseek_r1 = "deepseek-reasoner"
    deepseek_v2 = "deepseek-chat"

# VALID_OUTPUT_FORMATS = {"youtube", "tiktok"}

class TRANSCRIPTION_MODEL_NAMES(str, Enum):
    whisper = "whisper-1"

class OUTPUT_FORMATS(str, Enum):
    youtube = "youtube"
    tiktok = "tiktok"

DEFAULT_IMAGE_FORMAT = "png"

# https://platform.openai.com/docs/pricing
OPENAI_PRICING_MAP : dict[Enum, dict[str, float]] = {
    TEXT_MODEL_NAMES.openai_4o_mini : {
        "input" : .15,
        "output" : 0.6
    },
    TEXT_MODEL_NAMES.openai_4o: {
        "input" : 2.5,
        "output" : 10.0
    },
    TEXT_MODEL_NAMES.openai_o1 : {
        "input" : 15.0,
        "output" : 60.0
    },
    TEXT_MODEL_NAMES.openai_o1_mini : {
        "input" : 3.0,
        "output" : 12.0
    },
    TRANSCRIPTION_MODEL_NAMES.whisper : {
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

TEXT_GEN_BASE_URL : dict[Enum, str] = {
    TEXT_MODEL_COMPANY.openai : "https://api.openai.com/v1/",
    TEXT_MODEL_COMPANY.deepseek : "https://api.deepseek.com"
}

TEXT_GEN_API_KEY_NAME : dict[Enum, str] = {
    TEXT_MODEL_COMPANY.openai : "OPENAI_API_KEY",
    TEXT_MODEL_COMPANY.deepseek : "DEEPSEEK_API_KEY"
}

DEEPSEEK_PRICING_MAP : dict[Enum, dict[str,float]] = {
    TEXT_MODEL_NAMES.deepseek_v2 : {
        "input" : 0.14,
        "output" : 0.28
    },
    TEXT_MODEL_NAMES.deepseek_r1 : {
        "input" : 0.14,
        "output" : 2.19
    },
}

# Auth
TIKTOK_COOKIES_FILEPATH = "tiktok_auth/www.tiktok.com_cookies.txt"