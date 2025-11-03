import pyautogui
import os
import time
from datetime import datetime



def create_record_folder(base_dir="screenshots"):
    """Create a new timestamped folder for this recording session."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_name = f"record_{timestamp}"
    path = os.path.join(base_dir, folder_name)
    os.makedirs(path, exist_ok=True)
    return path

def record_screen(interval=1.0):
    """Continuously capture screenshots and save them with timestamps."""
    save_dir = create_record_folder()
    print(f"[INFO] Saving screenshots to: {save_dir}")
    print("[INFO] Press Ctrl + C to stop recording.")

    try:
        while True:
            # Create a timestamped filename
            filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")[:-3] + ".png"
            filepath = os.path.join(save_dir, filename)

            # Capture and save
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)

            print(f"[CAPTURED] {filename}")
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n[INFO] Recording stopped by user.")
        print(f"[INFO] Screenshots saved in: {save_dir}")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(os.getcwd())
    # record_screen(interval=1.0)  # 1 screenshot per second
    record_screen(interval=1/3)  # 1 screenshot per second
