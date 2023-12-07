import asyncio
import ssl
import pathlib
from websockets import serve

async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
pem = pathlib.Path(__file__).with_name("cert.pem")
key = pathlib.Path(__file__).with_name("key.pem")
ssl_context.load_cert_chain(pem, keyfile=key)

start_server = serve(echo, "localhost", 8765, ssl=ssl_context)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()