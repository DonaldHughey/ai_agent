import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_dir = os.path.abspath(working_directory)

        abs_file_path = os.path.normpath(
            os.path.join(abs_working_dir, file_path)
        )

        # Prevent directory traversal
        if os.path.commonpath(
            [abs_working_dir, abs_file_path]
        ) != abs_working_dir:
            return (
                f'Error: Cannot execute "{file_path}" '
                f'as it is outside the permitted working directory'
            )

        # File existence check
        if not os.path.isfile(abs_file_path):
            return (
                f'Error: "{file_path}" does not exist '
                f'or is not a regular file'
            )

        # Python file check
        if not file_path.lower().endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # Build command
        command = ["python", abs_file_path]

        if args:
            command.extend(args)

        # Run process
        result = subprocess.run(
            command,
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30
        )

        # Build output
        output = []

        if result.returncode != 0:
            output.append(
                f"Process exited with code {result.returncode}"
            )

        if not result.stdout and not result.stderr:
            output.append("No output produced")
        else:
            if result.stdout:
                output.append(f"STDOUT:\n{result.stdout}")

            if result.stderr:
                output.append(f"STDERR:\n{result.stderr}")

        return "\n".join(output)

    except subprocess.TimeoutExpired:
        return "Error: Process timed out after 30 seconds"

    except Exception as e:
        return f"Error running Python file: {e}"
    

schema_run_python_file= types.FunctionDeclaration(
name="run_python_file",
description="Runs a python file with the python interpreter. accepts additional cli args",
parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
        "file_path": types.Schema(
            type=types.Type.STRING,
            description="The file to run, relative to the working directory (default is the working directory itself)",
        ),
        "args": types.Schema(
            type=types.Type.ARRAY,
            description="An optional array of strings to be used as the CLI Args for the python file",
            items=types.Schema(
                type=types.Type.STRING
            ),
        ),
    },
),
)