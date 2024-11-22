import cv2
import socket
import numpy as np
import struct

"""
画像データを受信してGUIに表示する側
socket_server.py を実行する前にこの socket_client.py を先に実行して
この受信側を接続待受状態にしておく
"""
# 受信側のIPアドレスとポート番号
HOST = "10.32.130.87"  # picoのIPアドレス
PORT = 9002

# ソケットの作成
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # バインド
    s.bind((HOST, PORT))
    # 受信待機
    s.listen(1)
    print("Waiting for connection...")
    # 接続要求を受け入れる
    conn, addr = s.accept()
    with conn:
        print("Connected by", addr)
        while True:
            # フレームデータのサイズを受信
            data = conn.recv(4)
            if not data:
                break
            size = struct.unpack("!I", data)[0]
            # フレームデータを受信
            data = b""
            while len(data) < size:
                packet = conn.recv(size - len(data))
                if not packet:
                    break
                data += packet
            # 受信したデータをデコード
            frame_data = np.frombuffer(data, dtype=np.uint8)
            # データを画像に変換
            frame = cv2.imdecode(frame_data, 1)
            # 画像を表示
            cv2.imshow("frame", frame)
            # キー入力を待機
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
cv2.destroyAllWindows()
