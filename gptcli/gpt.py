import os
import sys
import openai
from openai import ChatCompletion
from dotenv import load_dotenv
from gptcli import console


SYSTEM_PROMPT = '''
You are a linux command-line expert. You are given a task to complete. You can use any linux command to complete the task. It is absolutely essential that you do not respond using any form of Markdown formatting. Instead, return a json string with two sections: "command" and "explanation".
Example:
User: Create a directory named "test" in the current directory.
Response:
{
    "command": "mkdir test",
    "explanation": "The mkdir command creates a directory. The -p flag creates any parent directories that do not exist."
}
'''


class Prompt:
    def __init__(self):
        self.prompt = [
            {
                'role': 'system',
                'content': SYSTEM_PROMPT,
            }
        ]

    def query(self, query):
        self.prompt.append({
            'role': 'user',
            'content': query,
        })

    def response(self, response):
        self.prompt.append({
            'role': 'assistant',
            'content': response,
        })


def gpt(prompt: Prompt):
    return ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=prompt.prompt,
        temperature=0.2,
    )['choices'][0]['message']['content']


def set_key():
    load_dotenv()
    key = os.getenv('OPENAI_API_KEY')
    if key:
        openai.api_key = key
    else:
        console.print(
            '''
            [red]No API key found.
            Please set the OPENAI_API_KEY environment variable or create a .env file in the project's root directory.
            Example:
            in `gptcli/.env`:
            OPENAI_API_KEY = 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
            '''
        )
        sys.exit(1)
