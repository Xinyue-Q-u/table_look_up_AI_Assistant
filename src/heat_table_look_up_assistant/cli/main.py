import click

from heat_table_look_up_assistant.cli.commands.chat import chat
from heat_table_look_up_assistant.cli.commands.config import config
# from heat_table_look_up_assistant.cli.commands.plan import plan
@click.group()
def cli():
    """Heat Table Look-up Assistant CLI"""
    # username and password validation
    # say hi
    pass


cli.add_command(chat)
cli.add_command(config)
# cli.add_command(plan)

def main():
    cli()

if __name__ == "__main__":
    main()