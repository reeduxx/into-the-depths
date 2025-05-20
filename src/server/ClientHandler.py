import threading

def handle_client(client, nickname, clients, nicknames, broadcast, start_combat_callback):
    try:
        while True:
            message = client.recv(1024).decode("ascii")
            print(f"[RECV from {nickname}] {message}")

            if message.lower().strip() == "combat":
                start_combat_callback()
            else:
                broadcast(f"{nickname}: {message}".encode("ascii"))
    except:
        if client in clients:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            left_nickname = nicknames.pop(index)
            broadcast(f"{left_nickname} left the game.".encode("ascii"))
