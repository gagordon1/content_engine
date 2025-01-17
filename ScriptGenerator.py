from ContentSpecs import ContentSpec
import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import TypedDict

load_dotenv()

class GeneratedScript(TypedDict):
    script: str
    prompt_tokens: int
    completion_tokens: int
    model_name: str

class ScriptGenerationError(Exception):
    """
    A generic error indicating that something went wrong during script generation.
    """

    def __init__(self, message: str):
        """
        :param message: A human-readable error message describing the issue.
        """
        super().__init__(message)


class ScriptGenerator:
    """
    ScriptGenerator is responsible for transforming source data and a user query
    into a formatted script. It can produce two main output formats:
      1) Video-oriented script
      2) Text-oriented post
    """

    def __init__(self, source_data : str, query : str, spec: ContentSpec, model_name = "gpt-4o-mini"):
        """
        Initialize the ScriptGenerator with:
          :param source_data: The textual foundation (str, dict, or other structure).
          :param query: A short description specifying style, tone, or key points.
          :param output_format: "video" or "text" (default is "text").
        """
        self.source_data = source_data
        self.query = query
        self.spec = spec
        self.model_name = model_name

    def generate_script(self) -> GeneratedScript: #type: ignore
        """
        Main entry point to produce a fully formed script based on self.source_data
        and self.query. If output_format is "video", includes scene directions,
        voiceover text, transitions, etc. If "text", produces paragraphs or bullet points.

        :return: A GeneratedScript containing string representing the final script, tokens used in prompt, and tokens used in completion
        :raises ScriptGenerationError: If an error occurs during the script creation process.
        """
        pass


    def generate_prompt(self):
        if self.spec.tone == "historian":
          prompt = self.source_data
          prompt += "\nYou are a Harvard educated historian, please summarize the content in a format suitable for a {} minute {} video".format(self.spec.duration, self.spec.output_format)
          prompt += "\nWhere appropriate describe an image to go along with the summary to create a montage. The image description should be separated by a '%^' string at the beginning and end of the caption. Ensure that each image caption has all required information to maintain continuity (each caption will get submitted on its own to an LLM to generate an image)"
          prompt += "\n In responding, please do not include additional symbols, formatting, titles etc. the response should just contain narration text and '%^' separated image captions"
        return prompt

class MontageScriptGenerator(ScriptGenerator):
    
    def __init__(self, source_data : str, query : str, spec: ContentSpec, model_name = "gpt-4o-mini"):
        super().__init__(source_data, query, spec, model_name=model_name)
    
    def generate_script(self) -> GeneratedScript:
        prompt = self.generate_prompt()
        client = OpenAI(
          api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
        )
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=self.model_name,
        )
        content = chat_completion.choices[0].message.content
        usage = chat_completion.usage
        if(usage) != None:
          prompt_tokens = usage.prompt_tokens
          completion_tokens = usage.completion_tokens
        if type(content) == str:
          return {
              "script": content,
              "prompt_tokens" : prompt_tokens,
              "completion_tokens" : completion_tokens,
              "model_name": self.model_name
          }
        else:
            raise ScriptGenerationError("Error during LLM script generation.")

if __name__ == "__main__":
    pass

