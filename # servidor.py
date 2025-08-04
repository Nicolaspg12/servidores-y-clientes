# servidor.py
import socket

HOST = '192.168.1.99'
PORT = 8000


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("[SERVIDOR] Esperando conexión...")

    conn, addr = s.accept()
    with conn:
        print(f"[SERVIDOR] Conexión establecida desde {addr}")

        data = conn.recv(1024)
        mensaje_recibido = data.decode('utf-8')
        print(f"[SERVIDOR] Mensaje recibido: {mensaje_recibido}")

        # Enviar respuesta
        respuesta = "Hola wenas las tenga fuerte y claro "
        conn.sendall(respuesta.encode('utf-8'))
        print("[SERVIDOR] Respuesta enviada")


