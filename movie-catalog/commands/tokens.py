from typing import Annotated

from api.api_v1.auth.services import redis_tokens
from rich import print
from rich.markdown import Markdown
import typer

app = typer.Typer(
    name="token",
    help="Tokens management",
    rich_markup_mode="rich",
    no_args_is_help=True,
)


@app.command()
def check(token: Annotated[str, typer.Argument(help="The token to check")]):
    """
    Check if the passed token is valid - exists or not.
    """
    print(
        f"Token [bold]{token}[/bold]",
        (
            "[green]exists[/green]."
            if redis_tokens.token_exists(token)
            else "[red]doesn't exist[/red]."
        ),
    )


@app.command(name="list")
def list_tokens():
    """
    List all tokens.
    """
    print(Markdown("# Available tokens:"))
    print(Markdown("\n1. ".join([""] + redis_tokens.get_tokens())))
    print()
