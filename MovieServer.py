# 画素数を落として
import cv2
import socket
import struct


# pico4の IP アドレスとポート番号
HOST = "10.32.130.87"
PORT = 9002

# ソケットの作成
cap = None
try:
    # カメラの準備
    cap = cv2.VideoCapture(1)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # サーバーに接続
        s.connect((HOST, PORT))
        while True:
            # 1フレーム分のデータをキャプチャ
            ret, frame = cap.read()
            if not ret:
                break

            # フレームの解像度を変更（例: 640x480）
            frame = cv2.resize(frame, (1080, 720))

            # フレームをJPEG形式でエンコード
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
            result, frame_data = cv2.imencode(".jpg", frame, encode_param)

            # フレームのサイズを取得
            size = len(frame_data)
            s.send(struct.pack("!I", size))  # フレームサイズを送信
            s.sendall(frame_data)  # フレームデータを送信

except BrokenPipeError as ex:
    print("BrokenPipeError: ", ex)

finally:
    if cap is not None:
        cap.release()
