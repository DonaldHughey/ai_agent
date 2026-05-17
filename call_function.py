from google.genai import types

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_files import write_file


def call_function(function_call, verbose=False):
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    function_map = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "write_files": write_file,
        "run_python_file": run_python_file,
    }

    function_name = function_call.name or ""

    # Handle unknown functions
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={
                        "error": f"Unknown function: {function_name}"
                    },
                )
            ],
        )

    # Make a shallow copy of args
    args = dict(function_call.args) if function_call.args else {}

    # Force working directory
    args["working_directory"] = "./calculator"

    # Call the function
    function_result = function_map[function_name](**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )