import argparse

from dotenv import load_dotenv

from commands import load_commands
from discord_client import run_discord_bot
from items import load_items


def main():
    parser = argparse.ArgumentParser(description='Run the Discord bot with specified environment.')
    parser.add_argument('--env', type=str, default='dev', help='The environment to use (e.g., dev, prod)')
    args = parser.parse_args()

    dotenv_path = f'.env.{args.env}'
    load_dotenv(dotenv_path)

    load_commands()
    load_items()

    run_discord_bot()


if __name__ == '__main__':
    main()
