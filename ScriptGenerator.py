from ContentSpecs import ContentSpec
import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import TypedDict
from constants import *
from prompts import *
import json

load_dotenv()

class MontageScriptFormat(TypedDict):
    image_prompts : list[str]
    narrations : list[str]

class GeneratedScript(TypedDict):
    script: str
    prompt_tokens: int
    completion_tokens: int
    model_name: str
    cost : float

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

    def __init__(self, source_data : str, spec: ContentSpec, model_name : TEXT_MODEL_NAMES, model_company : TEXT_MODEL_COMPANY):
        """
        Initialize the ScriptGenerator with:
          :param source_data: The textual foundation (str, dict, or other structure).
          :param query: A short description specifying style, tone, or key points.
          :param output_format: "video" or "text" (default is "text").
        """
        self.source_data = source_data
        self.spec = spec
        self.model_name = model_name
        self.model_company = model_company

    def generate_script(self) -> GeneratedScript: #type: ignore
        """
        Main entry point to produce a fully formed script based on self.source_data
        and self.query. If output_format is "video", includes scene directions,
        voiceover text, transitions, etc. If "text", produces paragraphs or bullet points.

        :return: A GeneratedScript containing string representing the final script, tokens used in prompt, and tokens used in completion
        :raises ScriptGenerationError: If an error occurs during the script creation process.
        """
        pass

    def calculate_cost(self, prompt_tokens : int, completion_tokens : int) -> float:
        
        if self.model_company == TEXT_MODEL_COMPANY.openai:
            cost_per_1m_prompt_token = OPENAI_PRICING_MAP[self.model_name]["input"]
            cost_per_1m_completion_token = OPENAI_PRICING_MAP[self.model_name]["output"]
        elif self.model_company == TEXT_MODEL_COMPANY.deepseek:
            cost_per_1m_prompt_token = DEEPSEEK_PRICING_MAP[self.model_name]["input"]
            cost_per_1m_completion_token = DEEPSEEK_PRICING_MAP[self.model_name]["output"]
        
        return (prompt_tokens * cost_per_1m_prompt_token + 
                completion_tokens * cost_per_1m_completion_token) / 10**6

class MontageScriptGenerator(ScriptGenerator):
    
    def __init__(self, source_data : str, spec: ContentSpec, 
                 model_name : TEXT_MODEL_NAMES, model_company : TEXT_MODEL_COMPANY):
        super().__init__(source_data, spec, model_name, model_company)
    
    def generate_prompt(self):
        source_data = self.source_data
        tone_prompt = TONE_MAP[self.spec.tone]
        return MONTAGE_NARRATION_FORMAT_PROMPT.format(
            source_data = source_data, 
            tone_prompt = tone_prompt, 
            duration = self.spec.duration, 
            output_format = self.spec.output_format)
    
    def generate_script(self) -> GeneratedScript:
        prompt = self.generate_prompt()
        client = OpenAI(
            api_key=os.environ.get(TEXT_GEN_API_KEY_NAME[self.model_company]),
            base_url= TEXT_GEN_BASE_URL[self.model_company]
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
              "model_name": self.model_name,
              "cost" : self.calculate_cost(prompt_tokens, completion_tokens)
          }
        else:
            raise ScriptGenerationError("Error during LLM script generation.")

if __name__ == "__main__":
    pass

