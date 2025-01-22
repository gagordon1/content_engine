import base64
import json
from constants import *

def save_string_as_text(file_path: str, data: str) -> None:
    """
    Saves a string to a plain text file in UTF-8 encoding.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(data)
def load_string_from_text(file_path: str) -> str:
    """
    Loads a string from a plain text file in UTF-8 encoding.

    :param file_path: The path to the text file.
    :return: The content of the file as a string.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    

def calculate_model_cost(prompt_tokens : int, completion_tokens: int, model_name : str) -> float:
    
    input_cost_per_1m = OPENAI_PRICING_MAP[model_name]["input"]
    output_cost_per_1m = OPENAI_PRICING_MAP[model_name]["output"]
    input_cost = prompt_tokens * input_cost_per_1m / 1000000
    output_cost = completion_tokens  * output_cost_per_1m / 1000000

    return input_cost + output_cost



def encode_png_to_base64(file_path: str) -> str:
    """
    Reads a PNG file from 'file_path' and returns a Base64-encoded string.
    """
    with open(file_path, "rb") as f:
        file_data = f.read()
    # Convert to Base64, then decode to get a string (instead of bytes)
    encoded_str = base64.b64encode(file_data).decode("utf-8")
    return encoded_str

def save_list_as_json(file_path: str, data_list: list) -> None:
    """
    Saves a Python list as a JSON file at the given file_path.

    :param file_path: Path where the JSON file should be created/overwritten.
    :param data_list: The Python list to be saved.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=2)

def load_list_from_json(file_path: str) -> list:
    """
    Loads a list from a JSON file and returns it.

    :param file_path: The path to the JSON file containing the list data.
    :return: A Python list reconstructed from the JSON file.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data_list = json.load(f)
    return data_list

def save_dict_as_json(file_path: str, data: dict) -> None:
    """
    Saves a Python list as a JSON file at the given file_path.

    :param file_path: Path where the JSON file should be created/overwritten.
    :param data_list: The Python dict to be saved.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_dict_from_json(file_path: str) -> dict:
    """
    Loads a dict from a JSON file and returns it.

    :param file_path: The path to the JSON file containing the list data.
    :return: A Python list reconstructed from the JSON file.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data
