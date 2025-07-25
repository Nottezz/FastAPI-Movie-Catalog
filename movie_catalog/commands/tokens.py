__all__ = ("app",)
from typing import Annotated

import typer
from api.api_v1.auth.services import redis_tokens
from rich import print
from rich.markdown import Markdown

app = typer.Typer(
    name="token",
    help="Tokens management",
    rich_markup_mode="rich",
    no_args_is_help=True,
)


@app.command()
def check(token: Annotated[str, typer.Argument(help="The token to check")]) -> None:
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
def list_tokens() -> None:
    """
    List all tokens.
    """
    print(Markdown("# Available tokens:"))
    print(Markdown("\n1. ".join([""] + redis_tokens.get_tokens())))
    print()


@app.command(name="create")
def create_token() -> None:
    """
    Create a new token.
    """
    print("Start creating a new token...")
    token = redis_tokens.generate_and_save_token()
    print(f"Token created: [bold]{token}[/bold]")


@app.command(name="delete")
def delete_token(
    token: Annotated[str, typer.Argument(help="The token to delete")],
) -> None:
    """
    Delete a token.
    """
    print("Start deleting a token...")
    if not redis_tokens.token_exists(token):
        print(f"Token [bold]{token}[/bold] [red]does not exist[/red].")
        return
    redis_tokens.delete_token(token)
    print(f"Token deleted: [bold]{token}[/bold]")


@app.command(name="add")
def add_token(token: Annotated[str, typer.Argument(help="The token to add")]) -> None:
    """
    Add token to database.
    """
    redis_tokens.add_token(token)
    print(f"Token added: [bold]{token}[/bold]")
