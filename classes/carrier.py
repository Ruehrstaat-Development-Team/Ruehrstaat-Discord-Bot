import json, os, requests, logging, time

from .service import Service as CarrierService

API_URL = 'https://api.ruehrstaat.de/api/v1/'
#API_URL = 'http://localhost:8000/api/v1/'

CARRIER_SERVICES = {}
CARRIER_INFO = {}

# request list of services from api
def getServices():
    url = API_URL + 'getAllServices'
    headers = {'Authorization': 'Bearer ' + os.getenv("READ_API_KEY")}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        services = json.loads(response.content)["services"]
        for service in services:
            CARRIER_SERVICES[service["name"]] = CarrierService(service["name"], service["label"], service["description"], bool(service["odyssey"]))
            logging.debug("Added Service: " + service["name"])
    else:
        return None
getServices()

def __getCarrierInfo():
    url = API_URL + 'getCarrierInfo?type=docking'
    headers = {'Authorization': 'Bearer ' + os.getenv("READ_API_KEY")}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # response json is a list of lists with name and label. save into CARRIER_INFO dict with .name and .label so it can be accessed by name
        CARRIER_INFO["dockingAccess"] = {dockingAccess[0]: {"name": dockingAccess[0], "label": dockingAccess[1]} for dockingAccess in json.loads(response.content)["dockingAccess"]}
    else:
        CARRIER_INFO["dockingAccess"] = {}
        return None
    
    url = API_URL + 'getCarrierInfo?type=category'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # response json is a list of lists with name and label. save into CARRIER_INFO dict with .name and .label so it can be accessed by name
        CARRIER_INFO["category"] = {category[0]: {"name": category[0], "label": category[1]} for category in json.loads(response.content)["carrierCategory"]}
    else:
        CARRIER_INFO["category"] = {}
        return None
__getCarrierInfo()

def getCarrierInfo():
    return CARRIER_INFO


class Carrier:
    def __init__(self, carrier_id):
        self.id = carrier_id
        self.name = None
        self.callsign = None
        self.current_location = None
        self.previous_location = None
        self.dockingAccess = None
        self.owner = None
        self.ownerDiscordID = None
        self.services = []
        self.last_update = time.time()
        self.imageURL = None
        self.category = None

    def setCarrierData(self, carrier_data):
        self.name = carrier_data["name"]
        self.callsign = carrier_data["callsign"]
        self.currentLocation = carrier_data["currentLocation"]
        self.previousLocation = carrier_data["previousLocation"]
        if carrier_data["dockingAccess"] in CARRIER_INFO["dockingAccess"]:
            self.dockingAccess = CARRIER_INFO["dockingAccess"][carrier_data["dockingAccess"]]

        self.owner = carrier_data["owner"]

        if carrier_data["ownerDiscordID"]:
            self.ownerDiscordID = int(carrier_data["ownerDiscordID"])
        self.imageURL = carrier_data["imageURL"]
        
        if carrier_data["category"] in CARRIER_INFO["category"]:
            self.category = CARRIER_INFO["category"][carrier_data["category"]]

        # save current timestamp as last update
        self.last_update = time.time()
        
        # go through carrier_data services, search for them in CARRIER_SERVICES and add them to self.services
        self.services = []
        for service in carrier_data["services"]:
            if service["name"] in CARRIER_SERVICES:
                self.services.append(CARRIER_SERVICES[service["name"]])

    def setCarrierOwnerDiscordID(self, ownerDiscordID, discord_id):
        self.ownerDiscordID = ownerDiscordID
        # write to api
        url = API_URL + 'carrier'
        headers = {'Authorization': 'Bearer ' + os.getenv("WRITE_API_KEY")}
        data = {
            "id": self.id,
            "ownerDiscordID": self.ownerDiscordID,
            "source": "discord",
            "discord_id": discord_id
        }
        response = requests.put(url, headers=headers, data=data)
        if response.status_code == 200:
            logging.debug("Successfully updated carrier ownerDiscordID in API")
        else:
            logging.error("Error updating carrier ownerDiscordID in API")

    def setCarrierLocation(self, location, discord_id):
        self.previousLocation = self.currentLocation
        self.currentLocation = location
        # write to api
        url = API_URL + 'carrier'
        headers = {'Authorization': 'Bearer ' + os.getenv("WRITE_API_KEY")}
        data = {
            "id": self.id,
            "currentLocation": self.currentLocation,
            "previousLocation": self.previousLocation,
            "source": "discord",
            "discord_id": discord_id
        }
        response = requests.put(url, headers=headers, data=data)
        if response.status_code == 200:
            logging.debug("Successfully updated carrier location in API")
            return True
        else:
            logging.error("Error updating carrier location in API")
            return False
        
    def setCarrierDockingAccess(self, dockingAccess, discord_id):
        if not dockingAccess in CARRIER_INFO["dockingAccess"]:
            logging.error("Invalid dockingAccess: " + dockingAccess)
            return False
        self.dockingAccess = CARRIER_INFO["dockingAccess"][dockingAccess]
        # write to api
        url = API_URL + 'carrier'
        headers = {'Authorization': 'Bearer ' + os.getenv("WRITE_API_KEY")}
        data = {
            "id": self.id,
            "dockingAccess": self.dockingAccess["name"],
            "source": "discord",
            "discord_id": discord_id
        }
        response = requests.put(url, headers=headers, data=data)
        if response.status_code == 200:
            logging.debug("Successfully updated carrier dockingAccess in API")
            return True
        else:
            logging.error("Error updating carrier dockingAccess in API")
            return False
        

    

    

    
