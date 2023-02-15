import websocket

async def carrierUpdater(websocket_url):
    async with websocket.connect(websocket_url) as carrierwebsocket:
        async for message in carrierwebsocket:
            await processWebsocketMessage(message)

async def processWebsocketMessage(message):
    if(message == "CarrierInfoUpdated"):
        print("updated")