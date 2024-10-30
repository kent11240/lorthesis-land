import importlib
import os

commands_registry = {}


def register_command(command, command_class):
    commands_registry[command] = command_class


def load_commands():
    command_files = [f[:-3] for f in os.listdir(os.path.dirname(__file__)) if f.endswith('_command.py')]
    for command_file in command_files:
        importlib.import_module(f'commands.{command_file}')
