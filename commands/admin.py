from nextcord import Interaction, SlashOption, Role, Permissions, Member, SelectOption
from nextcord.ui import Select, View
from helpfunctions import formatCarrierName
from caching import getCarrierIdByName, getCarrierObjectByID, getAllCarrierNames
from sqlalchemy.orm import Session
from database.engine import DB
import database.models as models
import logging
from embeds import getCarrierInfoStaticEmbed


def initAdminCommands(bot, args_dict):

    TESTING_GUILD_ID = args_dict["TESTING_GUILD_ID"]

    @bot.slash_command(name="registerrole", description="Registers a Role that can use the Bot", guild_ids=[TESTING_GUILD_ID], default_member_permissions=Permissions(administrator=True))
    async def registerRole(interaction: Interaction, roles: Role = SlashOption(name="roles", description="The Role that should be registered", required=True)):
        await interaction.response.send_message("Role registered")

    @bot.slash_command(name="setcarrierownerdiscordid", description="Sets the owner discord id of a specified Carrier", guild_ids=[TESTING_GUILD_ID], default_member_permissions=Permissions(administrator=True))
    async def setCarrierOwnerDiscordID(interaction: Interaction, captain: Member = SlashOption(name="user", description="The Owner of the Carrier", required=True), carrierName: str = SlashOption(name="carrier_name", description="The Carrier that get's a new Owner")):
        carrierName = formatCarrierName(carrierName)
        carrierid = getCarrierIdByName(carrierName, True)
        if carrierid == None:
            await interaction.response.send_message("Carrier not found!", ephemeral=True)
            return

        carrier = getCarrierObjectByID(carrierid)
        carrier.setCarrierOwnerDiscordID(captain.id, interaction.user.id)
        await interaction.response.send_message(f"Carrier Owner for {carrierName} set!", ephemeral=True)

    # Carrier channel command to set the channel for the static embeds

      # output: random shit

    @bot.slash_command(name="setcarrierchannel", description="Sets the channel for the static embeds", guild_ids=[TESTING_GUILD_ID], default_member_permissions=Permissions(administrator=True))
    async def setcarrierchannel(interaction: Interaction):
        # get all carrier names
        carrierNames = getAllCarrierNames()
        selectCarrier = Select(placeholder="Select a Carrier", options=[SelectOption(
            label=carrierNames[carrier], value=carrier) for carrier in carrierNames])

        selectmessage = None

        async def callback(interaction: Interaction):
            # get carrier id
            carrier_id = selectCarrier.values[0]
            if carrier_id == None:
                await interaction.response.send_message("Carrier not found!", ephemeral=True)
                return
            await selectmessage.delete()
            discord_channel = interaction.channel
            discord_guild = interaction.guild
            discord_role = await discord_guild.create_role(name="Passenger: " + getCarrierObjectByID(carrier_id).name)
            db = DB()
            with Session(db.engine) as session:
                channel = session.query(models.Discord_Channel).filter_by(
                    id=discord_channel.id).first()
                if (channel == None):
                    channel = models.Discord_Channel(id=discord_channel.id,
                                                    name=discord_channel.name,
                                                    jump_url=discord_channel.jump_url,
                                                    mention=discord_channel.mention)
                    guild = session.query(models.Discord_Guild).filter_by(
                        id=discord_guild.id).first()
                    if (guild == None):
                        guild = models.Discord_Guild(id=discord_guild.id,
                                             name=discord_guild.name)
                    channel.guild = guild
                else:
                    guild = channel.guild
                carrierDiscordChannel = models.Carrier_Discord_Channel(
                    carrier_market_id=carrier_id,
                    type="static",
                    channel=channel,
                    role=models.Discord_Role(
                        id=discord_role.id, name=discord_role.name, mention=discord_role.mention, managed=True, guild = guild)
                )
                session.add(carrierDiscordChannel)
                session.commit()
            logging.info(
                f"Carrier channel set to {discord_channel.id} for guild {discord_guild.id}")
            await interaction.response.send_message(f"Carrier Channel Set for Carrier " + getCarrierObjectByID(carrier_id).name, ephemeral=True)
            embed, view = getCarrierInfoStaticEmbed(carrier_id)
            await discord_channel.send(embed=embed, view=view)

            return None

        selectCarrier.callback = callback
        view = View()
        view.add_item(selectCarrier)
        selectmessage = await interaction.response.send_message("Select a Carrier", view=view, ephemeral=True)

        # TODO add Refresh Command for manual refresh of the marketname cache
