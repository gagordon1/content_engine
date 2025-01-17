import re
from ImageGenerator import StabilityImageGenerator
from ContentSpecs import VideoSpec
from utils import encode_png_to_base64

def parse_narration_and_captions(text: str) -> tuple[list[str], list[str]]:
    """
    Given a string that contains narration and image captions (delimited by %^ ... %^),
    return two lists:
      1) A list of narration segments (excluding content within %^ markers).
      2) A list of caption segments (the text found within %^ markers).

    :param text: The full raw text containing narration and %^ ... %^ caption blocks.
    :return: A tuple of two lists: (narration_list, caption_list).
    """

    # Regex to match all blocks between %^ ... %^ (including multiline).
    # We capture the text in a group so we can extract it as captions.
    pattern = r'%\^(.*?)%\^'  # Use parentheses to capture the content inside

    # 1. Find all caption blocks (the group inside %^...%^).
    captions = re.findall(pattern, text, flags=re.DOTALL)

    # 2. Remove the caption blocks from the original text, leaving only narration.
    #    We'll replace them with an empty string.
    narration_removed = re.sub(pattern, '', text, flags=re.DOTALL)

    # 3. Split narration into lines, stripping whitespace, keeping non-empty lines.
    narration_lines = [line.strip() for line in narration_removed.split('\n') if line.strip()]

    # 4. Similarly, split each caption into lines if desired, or keep them as raw blocks.
    #    For consistency, let's split them line-by-line as well and flatten or keep them separate.
    #    If you want each entire block as one entry, skip splitting by lines and just strip() them.
    caption_list = []
    for cap in captions:
        # Split by newline, remove blank lines
        lines = [line.strip() for line in cap.split('\n') if line.strip()]
        # If you prefer each entire caption block as one string, replace these 2 lines with:
        # lines = [cap.strip()]
        caption_list.extend(lines)

    return narration_lines, caption_list

class VideoGenerator:

    def __init__(self, script : str, video_spec : VideoSpec):
        self.script = script
        self.video_spec = video_spec
    
    def generate_video(self) -> str: #type: ignore
        pass

    def generate_image(self, caption : str, image : str | None = None) -> str:
        """Given an image caption generates the image and returns filepath 

        Args:
            caption (str): prompt for image generation model
            image (str): base64 encoded file of the image

        Returns:
            str: filepath of generated image
        """
        caption = "Make the folllowing caption in {} style ".format(self.video_spec.visual_art_style) + caption
        if self.video_spec.image_model_name and self.video_spec.image_model_name.split("-")[0] == "stability":
            image_path = StabilityImageGenerator().generate_image(caption, self.video_spec.get_aspect_ratio(),self.video_spec.image_model_name, self.video_spec.visual_art_style, image = image)
        else:
            raise Exception("Unsupported model selected in video spec.")
        return image_path


class MontageGenerator(VideoGenerator):

    def __init__(self, script : str, video_spec : VideoSpec):
        super().__init__(script, video_spec)
        self.narrations, self.image_captions = parse_narration_and_captions(script)
        assert len(self.narrations) == len (self.image_captions)

    def generate_video(self) -> str: 
        image = None
        for i in range(len(self.narrations)):
            narration = self.narrations[i]
            caption = self.image_captions[i]
            if image:
                image = self.generate_image(caption, image)
                print(image)
            else:
                image = self.generate_image(caption)
                print(image)
            if i == 1:
                break
        return ""

if __name__ == "__main__":
    pass
        