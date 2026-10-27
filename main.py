import os
import argparse
import json
import sys
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function

def main():

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    client = OpenAI(

        base_url = "https://openrouter.ai/api/v1",
        api_key=api_key,

    )

    parser = argparse.ArgumentParser(description="AgentAI Bot")
    parser.add_argument("user_prompt", type=str, help="User prompt for AgentAI Bot")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    if api_key == None: 
        raise RuntimeError("The API key is missing.")
    
    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            temperature=0,
            tools=available_functions
        )
        
        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls != None: 
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, args.verbose)
                if result_message["content"] == "": 
                    raise Exception("Missing content for this tool call")
                elif args.verbose == True: 
                    print(f"-> {result_message['content']}")
                messages.append(result_message)
        else: 
            print(f"Response: {message.content}")
            break
        
        if response.usage == None: 
            raise RuntimeError("The usage parameter is empty. API request failed.")
        elif args.verbose == True:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
    else:
        print("The agent couldn't finish the task within the range provided")
        sys.exit(1)

if __name__ == "__main__":
    main()
