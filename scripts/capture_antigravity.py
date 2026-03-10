import antigravity
import time
import pyautogui


def capture_screenshot():
    print("Capturing screenshot of the antigravity Easter egg in 5 seconds...")
    time.sleep(5)  # wait for the browser to open
    screenshot = pyautogui.screenshot()
    screenshot.save("demo/antigravity_screenshot.png")
    print("Screenshot saved to demo/antigravity_screenshot.png")


if __name__ == "__main__":
    capture_screenshot()
