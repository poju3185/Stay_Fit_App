# pip install opencv-python
import cv2  # 讀取圖片
# pip install pyzbar
from pyzbar.pyzbar import decode, ZBarSymbol
import time

# 選擇第三隻攝影機
cap = cv2.VideoCapture(0)

while(True):
  # 從攝影機擷取一張影像
  success, frame = cap.read()
  # 顯示圖片
  cv2.imshow('frame', frame)

  for code in decode(frame,symbols=[ZBarSymbol.QRCODE]):
      print(code.data.decode('utf-8'))
      time.sleep(3)

  # 若按下 q 鍵則離開迴圈
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

# 釋放攝影機
cap.release()

# 關閉所有 OpenCV 視窗
cv2.destroyAllWindows()