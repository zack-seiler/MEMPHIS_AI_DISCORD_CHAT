from discord.ext import commands


class HelpCogClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_message = """
```
Commands are currently unsupported
```
"""
        self.text_channel_list = []

    # some debug info so that we know the bot has started
    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                self.text_channel_list.append(channel)

        await self.send_to_all(self.help_message)

    @commands.command(name="help", help="Displays all the available commands")
    async def help(self, ctx):
        await ctx.send(self.help_message)

    async def send_to_all(self, msg):
        for text_channel in self.text_channel_list:
            await text_channel.send(msg)
