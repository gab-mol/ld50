import socket

# cliente
HOST, PORT = "127.0.0.1", 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
        s.connect((HOST, PORT))
except ConnectionError:
        print("\nFalla la conexión del cliente")

while True:
    print("\nEl cliente intenta enviar\n")
    try:
        s.sendall(b"Hola mundo")
    except:
        print("\nno manda un carajo\n")

    print("\nintenta responder el cliente:\n")
    data = s.recv(1024)
    print("\nRecibido de vuelta", repr(data))