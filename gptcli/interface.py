from os import chdir, system
from subprocess import run, CalledProcessError
from json import loads
from gptcli import console


def prompt_loop(wd, llm, prompt):
    with console.status('[bold green]Thinking...'):
        response = llm(prompt)
        prompt.response(response)

    try:
        response = loads(response)
        console.print(console.panels(**response))
    except Exception as e:
        prompt.query('Follow the appropriate JSON formatting!')
        prompt_loop(wd, llm, prompt)

    feedback = console.prompt('[bold]Any feedback? (Press enter to run)')
    if feedback:
        prompt.query(feedback)
        prompt_loop(wd, llm, prompt)
    else:
        chdir(wd)
        proc = run(
            response['command'],
            shell=True,
            check=False,
            capture_output=True,
        )
        stdout = proc.stdout.decode('utf-8')
        if proc.returncode:
            console.print('[bold red]Something went wrong')
            console.print(stdout)
            prompt.query(
                f'''
                That command failed with this traceback:
                {stdout}
                Provide a new command to fix this error.
                '''
            )
            console.print("[bold green]Let's see if I can figure it out...")
            prompt_loop(wd, llm, prompt)
        else:
            console.print(stdout)
