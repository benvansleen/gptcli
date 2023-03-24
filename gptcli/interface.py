from os import chdir, system
from sys import exit
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
        console.print(f'[bold red]Whoops, I might be stuck!')
        console.print(response)

        n_errors = prompt.json_error()
        if n_errors > 2:
            console.print(f"[bold red]I've had enough of this, goodbye!")
            exit(1)
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
        stderr = proc.stderr.decode('utf-8')
        if proc.returncode:
            console.print('[bold red]Something went wrong')
            console.print(stdout)
            console.print(stderr)
            if console.confirm('Do you want me to try to debug the error?'):
                prompt.debug(stdout, stderr)
                console.print("[bold green]Let's see if I can figure it out...")
                prompt_loop(wd, llm, prompt)
            else:
                console.print('[bold red]Exiting...')
                exit(1)
        else:
            console.print(stdout)
