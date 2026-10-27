import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str: 
    try:
        absolute_path_working_directory = os.path.abspath(working_directory)
        joined_paths = os.path.join(absolute_path_working_directory, directory)
        target_dir = os.path.normpath(joined_paths)
        valid_target_dir = os.path.commonpath([absolute_path_working_directory, target_dir]) == absolute_path_working_directory
        if valid_target_dir == False: 
            raise Exception(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        if not os.path.isdir(target_dir):
            raise Exception(f'Error: "{directory}" is not a directory')
        file_list = []
        for filename in os.listdir(target_dir):
            filepath = os.path.join(target_dir,filename)
            file_size = os.path.getsize(filepath)
            is_dir = os.path.isdir(filepath)
            result_string = f"  - {filename}: file_size={file_size} bytes, is_dir={is_dir}"
            file_list.append(result_string)
        return"\n".join(file_list)

    except Exception as e: 
        return(str(e))
