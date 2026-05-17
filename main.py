import argparse
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_files import schema_write_files
from functions.get_file_content import schema_get_file_content
from call_function import call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise Exception("Couldn't find api key in env")

    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`
    model_name = "gemini-2.5-flash"
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    available_functions = types.Tool(
    function_declarations=
    [schema_get_files_info, schema_get_file_content, schema_write_files, schema_run_python_file],
    
    )
    config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
    )
    response = client.models.generate_content(
    model=model_name,
    contents=messages,
    config=config,
    )
    if response.function_calls:
        function_results = []

        for function_call in response.function_calls:
            function_call_result = call_function(function_call, args.verbose)

            if not function_call_result.parts:
                raise Exception("Function call result has no parts")

            function_response = function_call_result.parts[0].function_response

            if function_response is None:
                raise Exception("Function call result has no function_response")

            if function_response.response is None:
                raise Exception("Function response has no response")

            function_results.append(function_call_result.parts[0])

            if args.verbose:
                print(f"-> {function_response.response}")
    else:
        print(response.text)

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        

main()
