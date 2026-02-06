from __future__ import annotations
import click

@click.group(help="View or modify assistant configuration")
def config():
    pass

@config.command("show",help="Print the current configuration")
@click.option("--json/--no-json",default=False,help="Print in Json format if supported")
def show(json:bool)->None:
    from heat_table_look_up_assistant.core.config import load_config,config_to_json
    cfg=load_config()
    if json:
        click.echo(config_to_json(cfg))
    else:
        click.echo(cfg)

@config.command("set", help="Set the configuration")
@click.argument("key")
@click.argument("value")
def set(key:str,value:str)->None:
    from heat_table_look_up_assistant.core.config import set_config_value
    set_config_value(key,value)
    click.echo(f"Set {key} to {value}")

@config.command("get", help="Get a configuration value")
@click.argument("key")
def get(key:str)->None:
    from heat_table_look_up_assistant.core.config import get_config_value
    value = get_config_value(key)
    click.echo(value)
@config.command("where",help="Show Config file location(if exists)")
def where()->None:
    from heat_table_look_up_assistant.core.config import get_config_path
    location=get_config_path()
    if location.exists():
        click.echo(location)
    else:
        click.echo("Config file not defined yet")