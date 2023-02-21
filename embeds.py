from nextcord import Embed, ButtonStyle
from nextcord.ui import View, Button

from caching import getCarrierObjectByID

from datetime import datetime

def getCarrierInfoEmbed(carrier_id):
    carrier = getCarrierObjectByID(carrier_id)
    embed = Embed(title=f"Carrier Info - {carrier.name} - {carrier.callsign}")
    embed.add_field(name="Current Location", value=carrier.currentLocation, inline=True)
    embed.add_field(name="Docking Access", value=carrier.dockingAccess["label"], inline=True)
    embed.add_field(name="Owner", value=carrier.owner, inline=True)

    # add services
    services = ""
    for service in carrier.services:
        services += f"{service.label}, "
    services = services[:-2]
    embed.add_field(name="Services", value=services, inline=False)
    # make embed side color #ffb400
    embed.colour = 0xffb400
    # add image
    embed.set_image(url=carrier.imageURL)
    # set footer
    embed.set_footer(text=f'last updated: {datetime.fromtimestamp(carrier.last_update).strftime("%d.%m.%Y %H:%M")} - powered by Ruehrstaat API')
    # Add carrier url as button
    view = View()
    if carrier.category == "flagship":
        view.add_item(Button(label="Carrier Website", url=f"https://ruehrstaat.de/carrier/{carrier.name.replace(' ', '-')}", style=ButtonStyle.success))
    else:
        view.add_item(Button(label="See all carriers", url=f"https://ruehrstaat.de/carrier/", style=ButtonStyle.success))
    return embed, view

def getCarrierInfoStaticEmbed(carrier_id):
    
    carrier = getCarrierObjectByID(carrier_id)
    embed = Embed(title=f"Carrier Info - {carrier.name} - {carrier.callsign}")
    embed.add_field(name="Current Location", value=carrier.currentLocation, inline=True)
    embed.add_field(name="Docking Access", value=carrier.dockingAccess["label"], inline=True)
    embed.add_field(name="Owner", value=carrier.owner, inline=True)

    # add services
    services = ""
    for service in carrier.services:
        services += f"{service.label}, "
    services = services[:-2]
    embed.add_field(name="Services", value=services, inline=False)
    # make embed side color #ffb400
    embed.colour = 0xffb400
    # add image
    embed.set_image(url=carrier.imageURL)
    # set footer
    embed.set_footer(text=f'last updated: {datetime.fromtimestamp(carrier.last_update).strftime("%d.%m.%Y %H:%M")} - powered by Ruehrstaat API')
    # Add carrier url as button
    view = View()
    if carrier.category == "flagship":
        view.add_item(Button(label="Carrier Website", url=f"https://ruehrstaat.de/carrier/{carrier.name.replace(' ', '-')}", style=ButtonStyle.success))
    else:
        view.add_item(Button(label="See all carriers", url=f"https://ruehrstaat.de/carrier/", style=ButtonStyle.success))
    getpassengerrole = "Placeholder" # TODO: Passengerroles from DB
    view.add_item(Button(label="Passenger-Role", style=ButtonStyle.success)) # TODO: Callback function
    return embed, view

def getCarrierListEmbed(carriers, isAdmin=False):
    embed = Embed(title="Carrier List")
    for carrierid in carriers:
        carrier = carriers[carrierid]
        fieldtext = f"Owner: {carrier.owner} - Callsign: {carrier.callsign}"
        if isAdmin:
            fieldtext += f" - ID: {carrier.id}"
        embed.add_field(name=carrier.name, value=fieldtext, inline=False)
    # make embed side color #ffb400
    embed.colour = 0xffb400
    # set footer
    embed.set_footer(text=f'powered by Ruehrstaat API')
    # Add carrier url as button
    view = View()
    view.add_item(Button(label="See all carriers", url=f"https://ruehrstaat.de/carrier/", style=ButtonStyle.success))
    return embed, view


def infoLinksEmbed():
    embed = Embed(title="Info Links")
    embed.color = 0xffb400
    embed.set_footer(text=f"Info by Ruherstaat Discord Bot")
    embed.add_field(name="Ruehrstaat Website", value="https://ruehrstaat.de", inline=False)
    embed.add_field(name="Ruhrstaat Carrier Website", value="https://ruehrstaat.de/carrier", inline=False)
    embed.add_field(name="ED Star Map", value="https://edsm.net", inline=False)
    embed.add_field(name="EDDB", value="https://eddb.io", inline=False)
    embed.add_field(name="EDMC", value="https://edmc.io", inline=False)
    embed.add_field(name="EDSY", value="https://edsy.org", inline=False)
    embed.add_field(name="Coriolis", value="https://coriolis.io", inline=False)
    embed.add_field(name="ED Shipyard", value="https://edshipyard.com", inline=False)
    embed.add_field(name="Inara", value="https://inara.cz", inline=False)
    embed.add_field(name="Commanders Toolbox", value="https://cmdrs-toolbox.com", inline=False)
    embed.add_field(name="Spansh", value="https://spansh.co.uk", inline=False)
    view = View()
    return embed, view