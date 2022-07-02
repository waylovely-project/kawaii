from typing import *
import click
from .build import available_buildsystems
class OrderedGroup(click.Group):
    def __init__(self, name=None, commands=None,  **attrs):
        super(OrderedGroup, self).__init__(name, commands, **attrs)

    def format_commands(self, ctx, formatter: click.HelpFormatter):
        super().get_usage(ctx)
        formatter.write_paragraph()

        main_commands = list()
        build_commands = list()
        
        for command in super().list_commands(ctx):
            if command in available_buildsystems:
                build_commands.append(command)
            else:
                main_commands.append(command)

        with formatter.section("The available commands are"):
            for command in main_commands:
                command: click.Command = super().get_command(ctx, command)
                desc = command.help.split("\n")[0]
                formatter.write_text(f"{command.name} - {desc}")
        
        with formatter.section("You can also directly execute build systems with Kawaii configurations!\n The available commands are"):
            formatter.write_text(", ".join(build_commands))