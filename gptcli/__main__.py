import openai
from sys import argv
from .interface import prompt_loop
from .gpt import gpt, Prompt, set_key


def start_query():
    wd = argv[1]
    query = ' '.join(argv[2:])
    prompt = Prompt()
    prompt.query(query)
    prompt_loop(wd, gpt, prompt)


def main():
    set_key()
    start_query()


if __name__ == '__main__':
    main()
