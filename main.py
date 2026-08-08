def main():
    import os
    import json
    from dotenv import load_dotenv
    import argparse
    from prompts import system_prompt
    from call_functions import available_functions, call_function

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key == None:
        raise RuntimeError("API Key not found")

    from openai import OpenAI

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    #get user prompt
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="Enter a prompt")

    #add option CLI --verbose
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    model = "openrouter/free"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    response = client.chat.completions.create(
        model=model, 
        messages=messages,
        tools=available_functions,)

    message = response.choices[0].message

    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, args.verbose)
            if result_message["content"] == None or result_message["content"] == "":
                raise Exception("No tool call content")
            if args.verbose:
                print(f"-> {result_message['content']}")
    else:
            print(response.choices[0].message.content)

    if args.verbose:
        if response.usage == None:
            raise RuntimeError("Failed API request")
        else:
            print(f"User prompt: {messages[0]["content"]}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
            print(f"Response:\n{response.choices[0].message.content}")

if __name__ == "__main__":
    main()
