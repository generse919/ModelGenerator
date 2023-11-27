import socket

def main():
    # サーバーのIPアドレスとポート
    server_ip = '0.0.0.0'  # 0.0.0.0はすべてのネットワークインターフェースを受け入れることを意味します
    server_port = 8086

    # UDPソケットを作成
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((server_ip, server_port))

    print(f'UDP server listening on {server_ip}:{server_port}')

    while True:
        # メッセージを受信
        data, address = server_socket.recvfrom(1024)
        message = data.decode('utf-8')
        print(f'Received message from client ({address}): {message}')

        # クライアントにメッセージを返信
        reply_message = 'Hello from server'
        server_socket.sendto(reply_message.encode('utf-8'), address)

if __name__ == "__main__":
    main()
