from nextcord import Interaction

def initFunCommands(bot, args_dict):

    TESTING_GUILD_ID = args_dict["TESTING_GUILD_ID"]

    @bot.slash_command(name="ping", description="Ping Command", guild_ids=[TESTING_GUILD_ID])
    async def ping(interaction: Interaction):
        await interaction.response.send_message("Pong", Ephemeral=True)

    