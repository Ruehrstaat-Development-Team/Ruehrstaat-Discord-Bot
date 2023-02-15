import logging
from os.path import isfile
from sqlalchemy import create_engine
import database.models as models


class DB:
    def __init__(self):
        self.engine = create_engine('sqlite:///bot.db', echo=True)

        try:
            if (not isfile('bot.db')):
                models.Base.metadata.create_all(self.engine)
        except Exception as e:
            logging.error("Failed to create database: " + str(e))
