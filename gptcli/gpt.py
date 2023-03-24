import os
import sys
import openai
from openai import ChatCompletion
from dotenv import load_dotenv
from gptcli import console
from .cache import check_cache, cache


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
        self.n_json_errors = 0
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

    def json_error(self):
        self.query('''
        Follow the appropriate JSON formatting!
        Example:
        User: Check for uncommitted changes in this repo
        Response:
        {
            "command": "git status",
            "explanation": "git status shows the status of the current git repo"
        }
        ''')
        self.n_json_errors += 1
        return self.n_json_errors

    def debug(self, stdout, stderr):
        self.query(f'''
        That command failed with this on stdout:
        {stdout}
        And this on stderr:
        {stderr}
        Provide a new command to fix this error.
        ''')


def gpt(prompt: Prompt):
    cached = check_cache(prompt.prompt)
    if cached:
        return cached
    else:
        print('Not in cache!')
        response = ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=prompt.prompt,
            temperature=0.2,
        )['choices'][0]['message']['content']
        cache(prompt.prompt, response)
        return response


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
