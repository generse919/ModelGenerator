# server_multi_thread.py
import socket
import sys
import errno
import threading
 
def server_socket(portnum):
    try:
        for res in socket.getaddrinfo(None, portnum, socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP, socket.AI_PASSIVE):
            af, socktype, proto, canonname, sa = res
            break
    except socket.gaieor as e:
        print("getaddrinfo():{}".format(e))
        sys.exit(1)
 
    try:
        nbuf, sbuf = socket.getnameinfo(sa, socket.AI_PASSIVE)
    except socket.gaieor as e:
        print("getnameinfo():{}".format(e))
        sys.exit(1)
 
    print("port={}".format(sbuf))
 
    try:
        soc = socket.socket(af, socktype, proto)
    except OSError as e:
        print("socket:{}".format(e))
        sys.exit(1)
 
    try:
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except OSError as e:
        print("setsockopt:{}".format(e))
        sys.exit(1)
 
    try:
        soc.bind(sa)
    except OSError as e:
        print("bind:{}".format(e))
        soc.close()
        sys.exit(1)
 
    try:
        soc.listen(socket.SOMAXCONN)
    except OSError as e:
        print("listen:{}".format(e))
        soc.close()
        sys.exit(1)
 
    return soc
 
def accept_loop(soc):
    while True:
        try:
            acc, addr = soc.accept()
            hbuf, sbuf = socket.getnameinfo(addr, socket.NI_NUMERICHOST | socket.NI_NUMERICSERV)
            print("accept:{}:{}".format(hbuf, sbuf))
            t = threading.Thread(target=send_recv, args=[acc])
            t.start()
                                
        except InterruptedError as e:
            if e.errno != errno.EINTR:
                print("accept:{}".format(e))
        except RuntimeError as e:
            print("thread:{}".format(e))
 
def send_recv(acc):
    buf_size = 512
    id = threading.get_ident()
    while True:
        try:
            data = acc.recv(buf_size)
        except InterruptedError as e:
            print("recv:{}".format(e))
            break 
 
        if (len(data) == 0):
            # EOF
            print("[{}]recv:EOF".format(id))
            break
 
        data = data.rstrip()
        try:
            print("[{}]{}".format(id, data.decode('utf-8')))
        except UnicodeDecodeError:
            pass
        try:
            acc.send(data + b':OK\r\n')
        except InterruptedError as e:
            print("send:{}".format(e))
            break
    acc.close()
 
if __name__ == '__main__':
    if (len(sys.argv) != 2):
        print("Usage: {} <server port>".format(sys.argv[0]))
        sys.exit(1)
 
    soc = server_socket(sys.argv[1])
 
    print("ready for accept")
 
    try:
        accept_loop(soc)
        soc.close()
    except KeyboardInterrupt:
        soc.close()
        sys.exit(1)