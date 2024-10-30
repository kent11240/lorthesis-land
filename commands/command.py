from abc import ABC, abstractmethod

import discord


class Command(ABC):
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    async def execute(self, message: discord.Message):
        pass
