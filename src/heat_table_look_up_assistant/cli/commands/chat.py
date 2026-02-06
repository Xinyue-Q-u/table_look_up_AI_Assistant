from __future__ import annotations

import click


@click.command(help="Ask the assistant a question(single or REPL)")
@click.argument("question", required=False)
# a default value can be set
@click.option("--model", default=None,help="Override the model")
@click.option("--stream/--no-stream", default=False)
def chat(question, model, stream):
    """
    Ask the assistant a question
    """
    pass
