import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_directory_abs, file_path))
        valid_file_path = os.path.commonpath([working_directory_abs, target_dir]) == working_directory_abs
        if valid_file_path == False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        else:
            if os.path.isdir(target_dir) == True:
                return f'Error: Cannot write to "{file_path}" as it is a directory'
            else:
                os.makedirs(os.path.dirname(target_dir), exist_ok=True)
                with open(target_dir, "w") as f:
                    f.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except OSError as e:
        return f'Error: {e}'