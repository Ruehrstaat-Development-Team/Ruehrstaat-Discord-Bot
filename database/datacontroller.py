from sqlalchemy.orm import Session
from database.engine import DB
import database.models as models

class datacontroller:
    def __init__(self):
        self.db = DB()
        self.session = Session(self.db.engine)


    def setCarrierStaticDiscordChannel(discord_channel, carrier_id): #TODO - GithubCoPilot pls fix
        with Session(self.db.engine) as session:
            channel = session.query(models.Discord_Channel).filter_by(
                id=discord_channel.id).first()
            if (channel == None):
                channel = models.Discord_Channel(id=discord_channel.id,
                                                name=discord_channel.name,
                                                jump_url=discord_channel.jump_url,
                                                carrier_id=carrier_id)
                session.add(channel)
            else:
                channel.carrier_id = carrier_id
            session.commit()
            return
        

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
    