import openai
from sys import argv
from os import getenv
from dotenv import load_dotenv
from .interface import prompt_loop
from .gpt import gpt, Prompt


def main():
    load_dotenv()
    openai.api_key = getenv('OPENAI_API_KEY')
    wd = argv[1]
    query = ' '.join(argv[2:])
    prompt = Prompt()
    prompt.query(query)
    prompt_loop(wd, gpt, prompt)


if __name__ == '__main__':
    main()
