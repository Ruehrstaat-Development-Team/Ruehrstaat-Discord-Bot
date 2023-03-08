from sqlalchemy.orm import Session
from database.engine import DB
import database.models as models
import logging
import caching
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from nextcord import TextChannel

class datacontroller:

    def setStaticCarrierChannel(request_channel: TextChannel, carrier_id: int):
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
            
            
        

    def setCarrierStaticDiscordRole(discord_role, carrier_id): #TODO - GithubCoPilot pls fix
        with Session(self.db.engine) as session:
            role = session.query(models.Discord_Role).filter_by(
                id=discord_role.id).first()
            if (role == None):
                role = models.Discord_Role(id=discord_role.id,
                                                name=discord_role.name,
                                                mention=discord_role.mention,
                                                carrier_id=carrier_id)
                session.add(role)
            else:
                role.carrier_id = carrier_id
            session.commit()
            return
    
    def setInfoChannel(discord_channel): #TODO - GithubCoPilot pls fix
        with Session(self.db.engine) as session:
            discord_channel = session.query(models.Discord_Channel).filter_by(
                id=discord_channel.id).first()
            if (channel == None):
                channel = models.Discord_Channel(id=discord_channel.id,
                                                name=discord_channel.name,
                                                jump_url=discord_channel.jump_url)
                session.add(channel)
            else:
                channel.info_channel = True
            session.commit()
            return     

    def getCarrierStaticDiscordChannel(carrier_id):  #TODO - GithubCoPilot pls fix
        with Session(self.db.engine) as session:
            discord_channel = session.query(models.Discord_Channel).filter_by(
                carrier_id=carrier_id).first()
            return discord_channel
        
    def getCarrierStaticDiscordRole(carrier_id):  #TODO - GithubCoPilot pls fix
        with Session(self.db.engine) as session:
            role = session.query(models.Discord_Role).filter_by(
                carrier_id=carrier_id).first()
            return role
        
    def getInfoChannel():
        with Session(self.db.engine) as session:    #TODO - GithubCoPilot pls fix
            discord_channel = session.query(models.Discord_Channel).filter_by(
                info_channel=True).first()
            return discord_channel
    