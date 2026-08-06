import os
def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_directory_abs, directory))
        valid_target_dir = os.path.commonpath([working_directory_abs, target_dir]) == working_directory_abs
        if os.path.isdir(target_dir) == False:
            return f'Error: "{target_dir}" is not a directory'
        else:
            if valid_target_dir == True:
               string = ""
               for items in os.listdir(target_dir):
                   try:
                       dir = os.path.join(target_dir, items)
                       name = os.path.basename(dir)
                       file_size = os.path.getsize(dir)
                       is_directory = os.path.isdir(dir)
                       string += f"  - {name}: file_size={file_size} bytes, is_dir={is_directory}\n"
                   except OSError as e:
                       return f"Error: {e}"
               if directory == ".":
                   directory_name = "current"
               else:
                   directory_name = directory  
               return f"Result for {directory_name} directory:\n{string}"
            else:
                return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    except OSError as e:
        return f"Error: {e}"