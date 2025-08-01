import socket
import threading

nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostname(), 55555))


def join_server(ip_string):
    octets = ip_string.split('.')
    print(octets)
    for num in octets:
        num = int(num)
    joined_ip = '.'.join(octets)
    print(joined_ip)


def receive():
    while True:
        try:
            message = client.recv(1024).decode("ascii")
            if message == 'NICK':
                client.send(nickname.encode("ascii"))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break

def write():
    while True:
        message = input("")
        client.send(message.encode("ascii"))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()