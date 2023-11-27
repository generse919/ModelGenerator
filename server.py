import socket
import os

def receive_jpeg_data(server_ip, server_port, save_path):
    # ソケットを作成
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(1)

    print(f"サーバーが {server_ip}:{server_port} で起動しました。")

    try:
        while True:
            print("クライアントの接続を待っています...")
            client_socket, client_address = server_socket.accept()
            print(f"クライアントが接続されました: {client_address}")

            # JPEGデータの受信
            jpeg_data = b""
            while True:
                chunk = client_socket.recv(1024)
                if not chunk or chunk.decode('utf-8') == "sendAllData":
                    break
                jpeg_data += chunk

            # 受信したJPEGデータをファイルに保存
            if jpeg_data:
                with open(save_path, 'wb') as file:
                    file.write(jpeg_data)
                print(f"JPEGデータを {save_path} に保存しました。")

            # クライアントとの接続を閉じる
            client_socket.close()
            print("クライアントとの接続を閉じました。")

    except KeyboardInterrupt:
        print("\nサーバーが終了しました。")

    finally:
        # ソケットを閉じる
        server_socket.close()

if __name__ == "__main__":
    # サーバーのIPアドレスとポート番号
    server_ip = "0.0.0.0"  # 任意のIPアドレスに変更
    server_port = 8086  # 任意のポート番号に変更

    # 受信したJPEGデータを保存するファイルパス
    save_path = "received_image.jpg"

    # JPEGデータの受信を開始
    receive_jpeg_data(server_ip, server_port, save_path)
