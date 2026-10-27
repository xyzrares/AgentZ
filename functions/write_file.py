import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes or overwrites a specified file with the provided content",
        "parameters": {
            "type": "object",
            "properties": {
                "content": { 
                    "type": "string",
                    "description": "This is the content that will be used in order to write/overwrite the file",
                },
                "file_path": {
                    "type": "string",
                    "description": "Path to the file of which content will be written/overwritten",
                },
            },
            "required": ["file_path", "content"]
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try: 
        abs_working_directory = os.path.abspath(working_directory)
        joined_paths = os.path.join(abs_working_directory, file_path)
        target_file = os.path.normpath(joined_paths)
        is_valid_target_file = os.path.commonpath([abs_working_directory, target_file]) == abs_working_directory
        if is_valid_target_file == False: 
            raise Exception(f'Cannot write to "{target_file}" as it is outside the permitted working directory')
        if os.path.isdir(target_file): 
            raise Exception(f'Cannot write to "{target_file}" as it is a directory')
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with open(target_file, mode='w') as f: 
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e: 
            return f'Error: {str(e)}'
