from loghook import LogHookBase
from dhooks import Webhook


class DiscordHook(LogHookBase):
    URL = "https://discord.com/api/webhooks/1234567890/abcdefghijklmnopqrstuvwxyz"

    def __init__(self):
        self.hook = Webhook.Async(self.URL)

    async def send(self, message: str):
        await self.hook.send(content=message, username="Oracle Cloud")

    async def close(self):
        await self.hook.close()
