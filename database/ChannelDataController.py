from sqlalchemy.orm import Session
from database.engine import DB
import database.models as models
import logging
import caching
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from nextcord import TextChannel, Guild

class ChannelDataController:

    #SECTION - Static Carrier Channel

    def getStaticCarrierChannels(request_guild: Guild, carrier_id: int):
        """Returns a list of all static channels in a Guild for a carrier"""
        with Session(DB().engine) as session:
            carrier_discord_channels = session.query(models.Carrier_Discord_Channel).filter_by(carrier_market_id=carrier_id, type="static").order_by(models.Carrier_Discord_Channel.channel.name).all()
            return carrier_discord_channels
        
    def getStaticCarrierRole(request_channel: models.Carrier_Discord_Channel, carrier_id: int):
        """Returns the static role for a channel"""
        with Session(DB().engine) as session:
            carrier_discord_channels = session.query(models.Carrier_Discord_Channel).filter_by(carrier_market_id=carrier_id, type="static", channel_id=request_channel.channel.id).one()
            return carrier_discord_channels.role

    def addStaticCarrierChannel(request_channel: TextChannel, carrier_id: int):
        """Sets a static channel for a carrier. If the combination of carrier and channel already exists, nothing will be changed."""
        with Session(DB().engine) as session:
            try:
                #Check if entry already exists
                session.query(models.Carrier_Discord_Channel).filter_by(carrier_market_id=carrier_id, type="static", channel_id=request_channel.id).one()
                logging.info("Entry for Carrier: " + carrier_id + " and Channel: " + request_channel.id + " already exists! No changes made!")
                return
            except MultipleResultsFound:
                #Multiple Results Found, log error (this should never happen)
                logging.error("Multiple entries for Carrier: " + carrier_id + " and Channel: " + request_channel.id + " found!")
                return
            except NoResultFound:
                #No Result found, create new entry
                channel = session.query(models.Discord_Channel).filter_by(id=request_channel.id).first()
                if(channel == None):
                    channel = models.Discord_Channel(id=request_channel.id, name=request_channel.name, jump_url=request_channel.jump_url, mention=request_channel.mention)
                    
                    guild = session.query(models.Discord_Guild).filter_by(id=request_channel.guild.id).first()
                    if(guild == None):
                        
                        guild = models.Discord_Guild(id=request_channel.guild.id, name=request_channel.guild.name)
                        channel.guild = guild
                #crate new Dicord Role for the static channel
                static_discord_role = request_channel.guild.create_role(name="Passenger " + caching.getCarrierObjectByID(carrier_id).name, reason="Static Role for Carrier " + caching.getCarrierObjectByID(carrier_id).name)
                role = models.Discord_Role(id=static_discord_role.id, name=static_discord_role.name, mention=static_discord_role.mention, managed=True)
                #create and save new Carrier_Discord_Channel
                carrier_discord_channel = models.Carrier_Discord_Channel(carrier_market_id=carrier_id, channel=channel, type="static", role=role)
                session.add(carrier_discord_channel)
                session.commit()
                return
    
    def deleteStaticCarrierChannel(request_channel: TextChannel, carrier_id: int):
        """Deletes a static channel for a carrier. If the combination of carrier and channel does not exist, nothing will be changed."""
        with Session(DB().engine) as session:
            try:
                #Check if entry already exists
                carrier_discord_channel = session.query(models.Carrier_Discord_Channel).filter_by(carrier_market_id=carrier_id, type="static", channel_id=request_channel.id).one()
                #Delete the entry
                session.delete(carrier_discord_channel)
                session.commit()
                return
            except MultipleResultsFound:
                #Multiple Results Found, log error (this should never happen)
                logging.error("Multiple entries for Carrier: " + carrier_id + " and Channel: " + request_channel.id + " found!")
                return
            except NoResultFound:
                #No Result found, log error
                logging.error("No entry for Carrier: " + carrier_id + " and Channel: " + request_channel.id + " found!")
                return
    
    #!SECTION - Static Carrier Channel
    #SECTION - Info Channel
    
    def getInfoChannel(request_guild: Guild):
        """Returns the info channel for a guild"""
        with Session(DB().engine) as session:
            discord_channel = session.query(models.Discord_Channel).filter_by(guild_id=request_guild.id, type="info").first()
            return discord_channel
    
    def setInfoChannel(request_channel: TextChannel):
        """Sets the info channel for a guild. If the guild already has an info channel defined, the old one will be overwritten."""
        with Session(DB().engine) as session:
            #Check if guild already has an info channel
            discord_channel = session.query(models.Discord_Channel).filter_by(guild_id=request_channel.guild.id, type="info").first()
            if(discord_channel == None):
                #No info channel found, create new one
                discord_channel = models.Discord_Channel(id=request_channel.id, name=request_channel.name, jump_url=request_channel.jump_url, mention=request_channel.mention, type="info")
                guild = session.query(models.Discord_Guild).filter_by(id=request_channel.guild.id).first()
                if(guild == None):
                    guild = models.Discord_Guild(id=request_channel.guild.id, name=request_channel.guild.name)
                    discord_channel.guild = guild
                session.add(discord_channel)
            else:
                #Info channel found, update it
                discord_channel.id = request_channel.id
                discord_channel.name = request_channel.name
                discord_channel.jump_url = request_channel.jump_url
                discord_channel.mention = request_channel.mention
            session.commit()
            return
    #!SECTION - Info Channel
    