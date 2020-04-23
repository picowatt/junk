import asyncio
import websockets
import json

def check_if_prime(num: int, arr: list) -> bool:
    check = int(num ** 0.5) + 1
    for i in arr:
        if i > check:
            break
        if num % i == 0:
            return False
    return True

async def calculate(websocket, path):
    cycle = 0
    primes = [2, 3]
    dimx = 1000
    dimy = 1000
    size = dimx * dimy

    while True:
        data = []
        for i in range(dimx):
            for j in range(dimy):
                ix = (cycle * size) + (i * dimx) + j
                if ix == 0 or ix == 1:
                    datum = 0xF0000000
                else:
                    if check_if_prime(ix, primes):
                        datum = 0xFFFFFFFF
                        primes.append(ix)
                    else:
                        datum = 0xF0000000
                data.append(datum)

        print("cycle {}".format(cycle))
        cycle = cycle + 1
        now = {"data" : data}
        print("send")
        await websocket.send(json.dumps(now))

start_server = websockets.serve(calculate, "127.0.0.1", 5678)

try:
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    pass