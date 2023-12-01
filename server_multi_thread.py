import socket
import threading
import decoder
import tempfile
from shap_e.mylib.modelCreate import model_create

class ModelGenerate:
    def __init__(self, host, port, recv_bytes, xm, model, diffusion):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = host
        self.port = port
        self.xm = xm
        self.model = model
        self.diffusion = diffusion
        self.argument = (self.host, self.port)
        self.sock.bind(self.argument)
        self.recv_bytes = recv_bytes
        self.clients = []
        self.address_bytes_map = {}
        

    def loop_handler(self, data, address):
        for value in self.clients:
            if value[1][0] == address[0] and value[1][1] == address[1]:
                # thread = threading.Thread(target=self.decodeData, args=(data, address), daemon=True)
                # thread.start()
                self.decodeData(data,address)
                # print("クライアント{}:{}から{}というメッセージを受信完了".format(value[1][0], value[1][1], data.decode()))
            else:
                value[0].sendto("クライアント{}:{}から{}を受信".format(value[1][0], value[1][1], data.decode()).encode("UTF-8"), address)

    def start_server(self):
        while True:
            try:
                data, addr = self.sock.recvfrom(self.recv_bytes)
                # アドレス確認
                print("[アクセス元アドレス]=>{}".format(addr[0]))
                print("[アクセス元ポート]=>{}".format(addr[1]))
                print("\r\n")
                # 待受中にアクセスしてきたクライアントを追加
                if not (self.sock, addr) in self.clients:
                    self.clients.append((self.sock, addr))
                self.loop_handler(data,addr)
                # スレッド作成
                # thread = threading.Thread(target=self.loop_handler, args=(data, addr), daemon=True)
                # スレッドスタート
                # thread.start()

            except KeyboardInterrupt:
                self.sock.close()
                exit()
    def decodeData(self,data:bytes,address):
        msg = data[0]
        id = data[1]
        print("msg: {},id: {},len: {}".format(msg,id,data.__len__()))
        if msg == int(decoder.MessageType.SENDFILE):
            print("receive file: id:{}".format(id))
            address_data = self.address_bytes_map.get(address, [])
            address_data += data[2:]
            self.address_bytes_map[address] = address_data
        elif msg == int(decoder.MessageType.SENDFILEEND):
            # 拡張子を取得する
            extension = data[2:].decode()
            print("receive end file: id:{}, extension:{}".format(id, extension))
            # Check if address is present in the dictionary
            if address in self.address_bytes_map:
                concatenated_bytes = b''.join(bytes(item) for item in self.address_bytes_map[address])
                # img_path = tempfile.NamedTemporaryFile(suffix=extension, delete=True, mode="w+b")
                # with open(img_path.name, 'wb') as f:
                with open("received_image.jpg", 'wb') as f:
                    f.write(concatenated_bytes)
                # model_create(self.xm, self.model, self.diffusion, img_path)
                # Remove the address entry after processing
                del self.address_bytes_map[address]
            else:
                print("Address not found in the dictionary.")
        else:
            print("メッセージタイプが不明です")



if __name__ == "__main__":
    model = ModelGenerate(host="0.0.0.0", port=8086, recv_bytes=8192)
    model.start_server()
