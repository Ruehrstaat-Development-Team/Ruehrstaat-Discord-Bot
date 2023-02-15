from nextcord import Interaction, SlashOption
from nextcord.ui import Select, View
from caching import getCarrierObjectByName
from helpfunctions import formatMarketItemName
from classes.market import MarketCommand




def initMarketCommands(bot, args_dict):
    
    TESTING_GUILD_ID = args_dict["TESTING_GUILD_ID"]

    @bot.slash_command(name="newtrade", description="Sets the embed for the market", guild_ids=[TESTING_GUILD_ID])
    async def newtrade(interaction: Interaction, carrier: str = SlashOption(name="carriername", description="Carrier Selection"), 
    marketitemname: str = SlashOption(name="commodity", description="Commodities Selection"), marketitemvalue: int = SlashOption(name="value", description="Value of the Commodity"), marketitemamount: int = SlashOption(name="amount", description="Amount of the Commodity"),
    station: str = SlashOption(name="station", description="Station Selection"), system: str = SlashOption(name="system", description="System Selection"), trade_type: str = SlashOption(name="tradetype", description="Trade Type Selection")):
        opened_by = interaction.user.mention
        owner = "PLACEHOLDER" # TODO: implement Command to get owner from Database
        if marketitemamount <= 0:
            await interaction.response.send_message("Amount must be greater than 0", ephemeral=True)
        else: 
            if marketitemvalue <= 0:
                await interaction.response.send_message("Value must be greater than 0", ephemeral=True)
            else: 
                carrier = getCarrierObjectByName(carrier)
                marketitemname = formatMarketItemName(marketitemname)
                channel_id = "PLACEHOLDER" # TODO: implement Command to get channel id from Database
                trade_type = trade_type

                marketnew = MarketCommand(carrier, marketitemname, marketitemamount, marketitemvalue, station, system, trade_type, opened_by, owner)
                await interaction.response.send_message(embed=marketnew.embed, view=marketnew.view)

