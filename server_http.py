from shap_e.mylib.modelCreate import model_create
import asyncio
import websockets
import os
import json
from threading import Thread
import tempfile
import time
import base64
import stat

class Server:
    def __init__(self, xm, model, diffusion):
        self.xm = xm
        self.model = model
        self.diffusion = diffusion
        self.client_data = {}

    async def handler(self, websocket,path):
        print("Client connected.")
        file_data = b''  # Initialize an empty byte string to hold the file data
        try:
            async for message in websocket:
                # print(f"Received message: {message}")  # Log received message
                data = json.loads(message)
                file_data += base64.b64decode(data['bytesBase64'])  # Append the received data to the file data
                filename = data['filename']
                client_id = data['clientId']

                if data['lastchunk'] == 'true' :  # If this is the last chunk of the file
                    self.client_data[client_id] = file_data  # Save the complete file data
                    _, extension = os.path.splitext(filename)  # Extract extension from filename
                    print(f"Received file: {extension}")  # Log received file
                    with open("received_image.jpg", 'wb') as f:
                        f.write(file_data)
                    img_temp = tempfile.NamedTemporaryFile(suffix=extension, delete=False)
                    # Process the file data...
                    with open(img_temp.name, 'wb') as f:
                        f.write(file_data)
                    img_temp.close()  # Close the file before passing its path to model_create

                 
                    # Notify the client that the model creation process is starting
                    await websocket.send(json.dumps({'status': 'model_creation_started'}))

                    # create model via shap_e
                    fbx_path = model_create(self.xm, self.model, self.diffusion, img_temp.name)

                    # Notify the client that the model creation process is finished
                    # await websocket.send(json.dumps({'status': 'model_creation_finished'}))

                    # Send the fbx file
                    chunksize = 1024  # You can set the chunk size as per your requirements
                    sequence = 0 # Initialize the sequence number
                    print("model path" + fbx_path)
                    # Check if the file exists and is readable
                    if not os.path.isfile(fbx_path):
                        print(f"Error: The file {fbx_path} does not exist.")
                        return
                   # Add read permission if not present
                    if not os.access(fbx_path, os.R_OK):
                        print(f"The file {fbx_path} is not readable. Adding read permission.")
                        os.chmod(fbx_path, stat.S_IRUSR)

                    # Now the file should be readable. If it's still not readable, there might be other issues (e.g., file is locked by another process)
                    if not os.access(fbx_path, os.R_OK):
                        print(f"Error: The file {fbx_path} is still not readable.")
                        return
                    with open(fbx_path, 'rb') as f:
                        print("read start:" + fbx_path)
                        total_bytes = 0
                        while True:
                            chunk = f.read(chunksize)
                            chunk_base64 = base64.b64encode(chunk)
                            # print("read" + str(chunk_base64))
                            # print("len: " + str(len(str(chunk_base64))))
                            total_bytes += len(chunk_base64)
                            if str(chunk_base64) == "b''":
                                print("sendEnd" + str(sequence))
                                print("Bytes: " + str(total_bytes))
                                await websocket.send(json.dumps({'status': 'model_creation_finished','sequence': sequence,'filename': filename}))
                                break
                            # print("send" + str(sequence))
                            await websocket.send(json.dumps({'status': 'model_creation_send',  'sequence': sequence,'filename': filename, 'chunksize': chunksize, 'filedata': chunk_base64.decode('utf-8')}))
                            sequence += 1
                pass
        except websockets.ConnectionClosed:
            print("Connection with client closed")
        except Exception as e:
            print(f"Error occurred: {e}")  # Log the error



# def start_server(server: Server):
#     async def server_coroutine():
#         server = await websockets.serve(server.handler, "0.0.0.0", 8086)
#         await server.wait_closed()

#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(server_coroutine())
#     loop.run_forever()

def start_server(server: Server):
    async def server_coroutine():
        print("Co Start.")  # Log server start
        try:
            websocket_server = await websockets.serve(server.handler, "0.0.0.0", 8086)
        except Exception as e:
            print(f"Error occurred: {e}")  # Log the error
            return
        print("Co Start2.")  # Log server start
        await websocket_server.wait_closed()
        print("Server closed.")  # Log server closedd

    print("Server started.")  # Log server started
    loop = asyncio.get_event_loop()
    # asyncio.set_event_loop(loop)
    loop.run_until_complete(server_coroutine())
    loop.run_forever()
    print("Server run.")  # Log server started
                        
# import asyncio
# import websockets

# async def echo(websocket, path):
#     message = await websocket.recv()
#     await websocket.send(message)

# async def main():
#     async with websockets.serve(echo, "0.0.0.0", 8086):
#         await asyncio.Future()
# def start_server(server: Server):
#     asyncio.run(main())