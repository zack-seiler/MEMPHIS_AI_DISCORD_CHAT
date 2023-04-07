import discord
from discord.ext import commands
import responses
from help_cog import HelpCogClass
import os


def read_token():
    file_name = "Discord_Bot_Token.txt"
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, file_name)
    with open(file_path, 'r') as file:
        token = file.readline().strip()
    return token


async def send_message(message, user_message, is_private, dummy_message=""):
    try:
        if not dummy_message:
            response = responses.handle_response(user_message, message.author, is_private)
            await message.author.send(response) if is_private else await message.channel.send(response)
        elif dummy_message:
            response = dummy_message
            await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)


def scan_for_command(text, char):
    index = text.find(char)
    if index != -1:
        return text[index:]
    else:
        return ""


def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.voice_states = True

    token = read_token()
    # client = discord.Client(intents=intents)
    client = commands.Bot(command_prefix="$M ", intents=intents)

    client.remove_command("help")

    desired_channel_id = 1086722654838460528
    memphis_bot_id = 1054520593753579651
    allowed_user_id = 192123570296455178

    @client.command()
    async def purge(ctx):
        # Replace 'your_user_id' with the ID of the user you want to grant access to the command

        if ctx.author.id == allowed_user_id:
            await ctx.send("Alright, sir. Purging the channel")
            while True:
                deleted = await ctx.channel.purge(limit=100)
                if len(deleted) < 100:
                    break
        else:
            await ctx.send("You do not have permission to use this command.")

    async def send_mod_dm(message_content):

        # Get the user object using the provided user ID
        target_user = await client.fetch_user(allowed_user_id)

        if target_user is None:
            print("User not found.")
            return
        try:
            # Send a DM to the user
            await target_user.send(message_content)
            print(f"Message sent to {target_user.name}.")
        except discord.Forbidden:
            print("Couldn't send a DM to the user.")

    @client.command()
    async def botban(ctx, user: discord.Member = None):

        if ctx.author.id == allowed_user_id or ctx.author.id == memphis_bot_id:
            botban_role_name = 'Botban'
            botban_role = discord.utils.get(ctx.guild.roles, name=botban_role_name)

            if user is None:
                await ctx.send("Please mention a user to timeout.")
                return
            if botban_role is None:
                await ctx.send(f"Role '{botban_role_name}' not found.")
                return

            await user.add_roles(botban_role)
            await ctx.send(f"{user.mention} has been botbanned")

    @client.event
    async def on_ready():
        await client.add_cog((HelpCogClass(client)))

        print(f'{client.user} is ready!')

    @client.event
    async def on_message(message):
        # await send_mod_dm(message_content="Howdy")
        # Check if the message contains a command
        ctx = await client.get_context(message)
        if ctx.valid:  # If the message contains a command, stop processing
            # Process command
            await client.process_commands(message)
            return

        if scan_for_command(message.content, "Epsilon2319") and ctx.author.id == memphis_bot_id:
            await send_mod_dm(message_content="Mod report: User needs to be botbanned")
            return

        # Checks to see if the message is the bot
        if message.author == client.user:
            return

        # Only proceed if the message is in the desired channel
        if message.channel.id == desired_channel_id or isinstance(message.channel, discord.DMChannel):

            # Set proper variables from the message object
            username = str(message.author)
            user_message = str(message.content)
            channel = str(message.channel)

            # Print for debugging
            print(f"{username} said: '{user_message}' ({channel})")

            # Check to see if the message begins with #M or if the message itself is a direct message.
            if user_message[:3] == '#M ' or isinstance(message.channel, discord.DMChannel):

                # Print for debugging
                print("Sending private to: " + username)

                # If message begins with #M, cut it out. Have to test twice for this, that's not good.
                if user_message[:3] == '#M ':
                    user_message = user_message[3:]

                # Send the message
                await send_message(message, user_message, is_private=True)

            # Otherwise, send to usual channel defined with desired_channel_id
            else:

                # Print for debugging
                print("Sending public to: " + channel)

                # Send the message
                await send_message(message, user_message, is_private=False)

    client.run(token)
