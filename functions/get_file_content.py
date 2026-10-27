import os
from config import MAX_CHAR_CAPACITY

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Prints the first 10000 characters of a file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file of which content will be shown",
                },
            },
            "required": ["file_path"]
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        absolute_working_directory = os.path.abspath(working_directory)
        joined_paths = os.path.join(absolute_working_directory, file_path)
        target_file = os.path.normpath(joined_paths)
        valid_target_file = os.path.commonpath([absolute_working_directory, target_file]) == absolute_working_directory
        if valid_target_file == False: 
            raise Exception(f'Error: Cannot read "{target_file}" as it is outside the permitted working directory')
        if os.path.isfile(target_file) == False: 
            raise Exception(f'Error: File not found or is not a regular file: "{file_path}"')
        
        with open(target_file) as f:
            content = f.read(MAX_CHAR_CAPACITY)
            if f.read(1):
                content += f'[...File "{target_file} truncated at {MAX_CHAR_CAPACITY} characters"]'
            return content
    except Exception as e:
         return(str(e))

