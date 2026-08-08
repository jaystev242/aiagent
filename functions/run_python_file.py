import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_directory_abs, file_path))
        valid_file_path = os.path.commonpath([working_directory_abs, target_dir]) == working_directory_abs
        if valid_file_path == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        else:
            if os.path.isfile(target_dir) == False:
                return f'Error: "{file_path}" does not exist or is not a regular file'
            else:
                if file_path.endswith('.py') == False:
                    return f'Error: "{file_path}" is not a Python file'
                else:
                    command = ["python", target_dir]
                    if args is not None and len(args) >= 1:
                        command.extend(args)
                    runcommand = subprocess.run(command, cwd=os.path.dirname(target_dir), capture_output=True, timeout=30, text=True)
                    if runcommand.returncode != 0:
                        string = f'Process exited with code {runcommand.returncode}'
                    elif runcommand.stdout == "" and runcommand.stderr == "":
                        string = 'No output produced'
                    else:
                        string = f'STDOUT: {runcommand.stdout}\nSTDERR: {runcommand.stderr}'
                    return string
    except OSError as e:
        return f'Error: executing Python file: {e}'


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs specified python file in working directory/file path",
        "parameters": {
            "type": "object",
            "properties": {
                "working_directory": {
                    "type": "string",
                    "description": "Working directory",
                },
                "file_path": {
                    "type": "string",
                    "description": "path to file",
                },
                "args": {
                    "type": "list[string]",
                    "description": "list of arguments to be passed to function",
                },
            },
        },
    },
}