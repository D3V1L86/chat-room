import socket
from threading import Thread

print("\n")
print("""
██████╗██╗  ██╗ █████╗ ████████╗   ██████╗  ██████╗  ██████╗ ███╗   ███╗
██╔════╝██║  ██║██╔══██╗╚══██╔══╝   ██╔══██╗██╔═══██╗██╔═══██╗████╗ ████║
██║     ███████║███████║   ██║█████╗██████╔╝██║   ██║██║   ██║██╔████╔██║
██║     ██╔══██║██╔══██║   ██║╚════╝██╔══██╗██║   ██║██║   ██║██║╚██╔╝██║
╚██████╗██║  ██║██║  ██║   ██║      ██║  ██║╚██████╔╝╚██████╔╝██║ ╚═╝ ██║
 ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝      ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝     ╚═╝
 \n  
        \033[33m Developpeur : https://github.com/haisenberg\033[33m""")
print("\n")

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002 
separator_token = "<SEP>" 

client_sockets = set()

s = socket.socket()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((SERVER_HOST, SERVER_PORT))

s.listen(5)
print(f"[*] Le serveur {SERVER_HOST}:{SERVER_PORT} a été mis en route")

def listen_for_client(cs):
    """
    Cette fonction continue d'écouter un message de la socket `cs`
    Chaque fois qu'un message est reçu, diffusez-le à tous les autres clients connectés
    """
    while True:
        try:

            msg = cs.recv(1024).decode()
        except Exception as e:


            print(f"[!] Erreur : {e}")
            client_sockets.remove(cs)
        else:


            msg = msg.replace(separator_token, ": ")

        for client_socket in client_sockets:

            client_socket.send(msg.encode())


while True:

    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connecté avec succès.")

    client_sockets.add(client_socket)

    t = Thread(target=listen_for_client, args=(client_socket,))

    t.daemon = True

    t.start()


for cs in client_sockets:
    cs.close()

s.close()
