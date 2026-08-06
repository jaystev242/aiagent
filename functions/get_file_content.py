import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_directory_abs, file_path))
        valid_file_path = os.path.commonpath([working_directory_abs, target_dir]) == working_directory_abs
        if valid_file_path == False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        else:
            if os.path.isfile(target_dir) == False:
                return f'Error: File not found or is not a regular file: "{file_path}"'
            else:
                with open(target_dir, "r") as f:
                     content = f.read(MAX_CHARS)
                     # After reading the first MAX_CHARS...
                     if f.read(1):
                         content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content
    except OSError as e:
        return f'Error: {e}'
