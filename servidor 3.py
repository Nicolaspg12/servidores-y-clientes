import socket
import cv2
import numpy as np
from ultralytics import YOLO  # Asegúrate de tener `ultralytics` instalado: pip install ultralytics

def receive_frames_and_segment(host='', port=8000, model_path= r'C:\Users\santi\Downloads\wine\xd\yolov8n.pt'):
    server_socket = socket.socket()
    conn = None

    try:
        # Cargar modelo YOLOv8
        model = YOLO(model_path)  # Asegúrate de que este sea un modelo YOLOv8-seg

        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"[Servidor] Esperando conexión en {host}:{port}...")

        conn, addr = server_socket.accept()
        print(f"[Servidor] Conectado con {addr}")

        data = b''
        payload_size = 4

        while True:
            while len(data) < payload_size:
                packet = conn.recv(4096)
                if not packet:
                    raise ConnectionError("Conexión cerrada por el cliente.")
                data += packet
            frame_size = int.from_bytes(data[:4], byteorder='big')
            data = data[4:]

            while len(data) < frame_size:
                packet = conn.recv(4096)
                if not packet:
                    raise ConnectionError("Conexión cerrada por el cliente.")
                data += packet

            frame_data = data[:frame_size]
            data = data[frame_size:]

            frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)

            # ➤ Segmentación con YOLOv8
            results = model.predict(source=frame, task='segment', imgsz=640, conf=0.5, verbose=False)
            annotated_frame = results[0].plot()

            cv2.imshow("Segmentación YOLOv8", annotated_frame)
            if cv2.waitKey(1) == 27:  # ESC
                print("[Servidor] ESC presionado. Saliendo...")
                break

    except KeyboardInterrupt:
        print("[Servidor] Interrupción por teclado.")

    except Exception as e:
        print(f"[Servidor] Error: {e}")

    finally:
        print("[Servidor] Liberando recursos...")
        if conn:
            conn.close()
        server_socket.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    receive_frames_and_segment(model_path='best.pt')  # Asegúrate que 'best.pt' sea tu modelo YOLOv8-seg
