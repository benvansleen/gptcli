from rich import box
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.align import Align
from rich.console import Group


console = Console()


def panels(command, explanation, **kwargs):
    return Group(
        Align.center(
            Panel.fit(
                command,
                title='Command',
                style='bold blue',
                box=box.HORIZONTALS,
            ),
            vertical='middle',
        ),
        Align.center(
            Panel.fit(
                explanation,
                title='Explanation',
                style='red',
                box=box.HORIZONTALS,
            ),
            vertical='middle',
        )
    )


console.prompt = Prompt.ask
console.confirm = Confirm.ask
console.panels = panels
