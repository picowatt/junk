import asyncio
import websockets
import uuid

socks = []

async def forward(websocket, path):
    socks.append(websocket)
    print("added")
    me = uuid.uuid4()

    while True:
        data = await websocket.recv()
        await asyncio.wait([ws.send(data) for ws in socks])
        print("{} sent".format(me))


start_server = websockets.serve(forward, "127.0.0.1", 5678, max_size=None)

try:
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    pass