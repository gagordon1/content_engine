from constants import *
from typing import Literal

class ContentSpec:

    def __init__(self, type: str, tone: str, 
                    output_format: OUTPUT_FORMATS, 
                    duration: float, 
                    visual_art_style : VISUAL_ART_STYLES,
                    image_model_name : IMAGE_MODEL_NAMES | None = None):
        """
        :param type: Category/kind of content (e.g. 'slideshow', 'montage').
        :param tone: The style or mood (e.g. 'dramatic', 'friendly').
        :param output_format: The desired output file format (e.g. 'mp4').
        :param duration: The approximate length of the video in seconds (must be >= 0).
        :param visual_art_style: one of 3d-model analog-film anime cinematic comic-book digital-art enhance fantasy-art isometric line-art low-poly modeling-compound neon-punk origami photographic pixel-art tile-texture
        :param image_model_name: Valid image model name.

        Raises:
            ValueError: If any input fails the required checks.
        """

        # Check 'type' against allowed set
        if type not in CONTENT_TYPES:
            raise ValueError(f"type must be one of {CONTENT_TYPES}, got '{type}'.")
        self.type = type

        # Check 'tone' against allowed set
        if tone not in CONTENT_TONES:
            raise ValueError(f"tone must be one of {CONTENT_TONES}, got '{tone}'.")
        self.tone = tone

        # Check 'output_format' against allowed set
        if output_format not in OUTPUT_FORMATS:
            raise ValueError(f"output_format must be one of {OUTPUT_FORMATS}, got '{output_format}'.")
        self.output_format = output_format

        # Duration check (must be non-negative)
        if not isinstance(duration, (int, float)) or duration < 0:
            raise ValueError(f"duration must be a non-negative number, got {duration}.")
        self.duration = float(duration) 

        if visual_art_style not in VISUAL_ART_STYLES:
            raise ValueError(f"visual art style must be one of {VISUAL_ART_STYLES}, got '{visual_art_style}'.")
        self.visual_art_style = visual_art_style

        if image_model_name and image_model_name not in IMAGE_MODEL_NAMES:
            raise ValueError(f"image model name must be one of {IMAGE_MODEL_NAMES}, got '{image_model_name}'.")
        self.image_model_name = image_model_name

class VideoSpec(ContentSpec):
    """
    A specification class that holds key information about a video request,
    including query, type, tone, output format, and duration.
    It performs basic checks on the input values to ensure they are valid.
    """

    def __init__(self, type, tone, output_format, duration, visual_art_style, image_model_name):
        super().__init__(type, tone, output_format, duration, visual_art_style, image_model_name)

    def get_aspect_ratio(self):
        return ASPECT_RATIOS[self.output_format]

    def __repr__(self):
        return (
            f"VideoSpec(type={self.type!r}, "
            f"tone={self.tone!r}, output_format={self.output_format!r}, "
            f"duration={self.duration})"
        )
