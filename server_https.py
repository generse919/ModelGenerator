import asyncio
import ssl
import pathlib
from websockets import serve

async def echo(websocket, path):
    async for message in websocket:
        print(f"Received message: {message}")  # Log received message
        await websocket.send(message)
        print(f"Sent message: {message}")  # Log sent message

print("Setting up SSL context...")  # Log SSL setup
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
pem = pathlib.Path(__file__).parent / "configs/certs/cert.pem"
key = pathlib.Path(__file__).parent / "configs/certs/key.pem"
ssl_context.load_cert_chain(pem, keyfile=key)

async def main():
    print("Starting server...")  # Log server start
    start_server = serve(echo, "0.0.0.0", 8086, ssl=ssl_context)
    server = await start_server
    print("Server started.")  # Log server started
    await server.wait_closed()

print("Running main function...")  # Log main function start
asyncio.run(main())
print("Main function finished.")  # Log main function end