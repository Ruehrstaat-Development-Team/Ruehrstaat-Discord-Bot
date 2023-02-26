from caching import getAllCarrierNamesAsList
from difflib import get_close_matches
import logging
from embeds import getCarrierInfoStaticEmbed
from nextcord import Interaction

def formatCarrierName(carrierName):
    if not carrierName.startswith("RST "):
        carrierName = "RST " + carrierName
    carrierNames = getAllCarrierNamesAsList()
    if carrierName in carrierNames:
        return carrierName
    matches = get_close_matches(carrierName, carrierNames, n=1, cutoff=0.8)
    if len(matches) > 0:
        carrierName = matches[0]
        return carrierName
    return None


# TODO: carrier refresh method to refresh the static embeds with args from the websocket event or nothing to refresh all
def refreshCarrierEmbeds(bot, args_dict, carrier_id=None):
    db = args_dict["db"]
    cursor = db.cursor
    logging.info("refreshing carrier embeds")
    cursor.execute("SELECT * FROM guilds WHERE carrier_id = ?", (carrier_id))
    db_object = cursor.fetchone()
    embed, view = getCarrierInfoStaticEmbed(carrier_id)
    bot.getChannel(db_object.carrier_channel_id).send(embed=embed, view=view)
    

# TODO: implement Formatter for Market item Names
def formatMarketItemName(marketitemname):
    return marketitemname

async def assignPassengerRole(interaction: Interaction): #TODO: Get Passenger Role from DB
    passengerrole = interaction.guild.get_role(983078188773154837)
    await interaction.user.add_roles(passengerrole)
    await interaction.response.send_message("You are now a passenger!", ephemeral=True)
    return None