import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        abs_working_dir = os.path.abspath(working_directory)

        target_dir = os.path.abspath(
            os.path.join(abs_working_dir, directory)
        )

        if os.path.commonpath([abs_working_dir, target_dir]) != abs_working_dir:
            return (
                f'Error: Cannot list "{directory}" '
                f'as it is outside the permitted working directory'
            )

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        results = []

        for item_name in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item_name)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)

            results.append(
                f"- {item_name}: file_size={file_size} bytes, is_dir={is_dir}"
            )

        return "\n".join(results)

    except Exception as e:
        return f"Error: {e}"
    

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)