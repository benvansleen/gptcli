import openai
from sys import argv, exit
from .interface import prompt_loop
from .gpt import gpt, Prompt, set_key


def start_query():
    wd = argv[1]
    query = ' '.join(argv[2:])
    prompt = Prompt()
    prompt.query(query)
    prompt_loop(wd, gpt, prompt)


def main():
    try:
        set_key()
        start_query()
    except KeyboardInterrupt:
        exit(0)


if __name__ == '__main__':
    main()
