from loghook import LogHookBase
from dhooks import Webhook


class DiscordHook(LogHookBase):
    URL = "https://discord.com/api/webhooks/1234567890/abcdefghijklmnopqrstuvwxyz"

    def __init__(self):
        self.hook = Webhook.Async(self.URL)

    async def send(self, *args, **kwargs):
        if not kwargs.get("username"):
            kwargs["username"] = "Oracle Cloud (LaunchInstance)"
        await self.hook.send(*args, **kwargs)

    async def close(self):
        await self.hook.close()
