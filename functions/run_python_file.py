import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a .py file and can accept optional command-line arguments",
        "parameters": {
            "type": "object",
            "properties": {
                "args": {
                    "type": "array",
                    "description": "An optional list of command-line arguments passed to the Python script.",
                    "items": {
                        "type": "string"
                    },
                },
                "file_path": {
                    "type": "string",
                    "description": "Path to the file that will be executed",
                },
            },
            "required": ["file_path"]
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        abs_working_directory = os.path.abspath(working_directory)
        joined_paths = os.path.join(abs_working_directory, file_path)
        target_file = os.path.normpath(joined_paths)
        is_valid_target_file = os.path.commonpath([abs_working_directory, target_file]) == abs_working_directory
        if is_valid_target_file == False: 
            raise Exception(f'Cannot execute "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(target_file): 
            raise Exception(f'"{file_path}" does not exist or is not a regular file')
        if target_file[-3:] != ".py":
            raise Exception(f'"{file_path}" is not a Python file')

        command = ["python", target_file]
        if args:
            command.extend(args)
        
        try:
            process = subprocess.run(command, cwd=abs_working_directory, timeout=30, capture_output=True, text=True)
            stdout_v, stderr_v, returncode_err = process.stdout, process.stderr, process.returncode
            error_string = ""
            if len(stdout_v) > 0: 
                error_string += "STDOUT: " + stdout_v + '\n'
            if len(stderr_v) > 0: 
                error_string += "STDERR: " + stderr_v + '\n'
            if returncode_err != 0:
                error_string += f"Process exited with code {returncode_err}\n"
            if stdout_v == "" and stderr_v == "":
                error_string += "No output produced\n"
            return error_string
        except Exception as e: 
            return f"Error: executing Python file: {e}"
    
    except Exception as e: 
        return f"Error: {e}"
