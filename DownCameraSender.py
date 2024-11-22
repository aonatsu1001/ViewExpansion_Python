import socket
import cv2
import numpy as np
import struct
import time
import threading

# カメラのセットアップ
# camera1 = cv2.VideoCapture(2)  # 左クワッド
# camera2 = cv2.VideoCapture(0)  # 右クワッド
camera3 = cv2.VideoCapture(1)  # 下クワッド
if not camera3.isOpened():
    print("Failed to open one or both cameras")
    exit()

def send_camera_stream(camera, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("10.32.130.79", port))
    server_socket.listen(0)
    print(f"Waiting for connection on port {port}...")

    client_socket, addr = server_socket.accept()
    print(f"Connection from: {addr} on port {port}")

    try:
        while True:
            ret, frame = camera.read()
            if not ret:
                print("Failed to capture frame")
                break

            frame = cv2.resize(frame, (1080, 720))
            success, jpeg_frame = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 95]) # 画質を95に設定
            if not success:
                print("Failed to encode frame")
                continue

            data = jpeg_frame.tobytes()
            size = len(data)
            print(f"Sending frame of size: {size} on port {port}")

            # エンディアン設定をC#と一致させる (ビッグエンディアン)
            client_socket.sendall(struct.pack(">I", size) + data)

    except Exception as e:
        print(f"Error during frame processing or sending: {e}")
    finally:
        camera.release()
        client_socket.close()
        server_socket.close()
        print(f"Finished on port {port}")

# 二台のカメラストリームを別々のスレッドで送信
# thread1 = threading.Thread(target=send_camera_stream, args=(camera1, 9002))
# thread2 = threading.Thread(target=send_camera_stream, args=(camera2, 9001))
thread3 = threading.Thread(target=send_camera_stream, args=(camera3, 9003))

# thread1.start()
# thread2.start()
thread3.start()

# thread1.join()
# thread2.join()
thread3.join()
