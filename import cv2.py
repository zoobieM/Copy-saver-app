import cv2
import os
import time
import numpy as np

def convert_frame_to_ascii(frame, width=80):
    ascii_chars = " .:-=+*#%@"
    height = int(frame.shape[0] * width / frame.shape[1] / 2)
    if height == 0:
        height = 1
    resized_frame = cv2.resize(frame, (width, height))
    if len(resized_frame.shape) > 2:
        gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
    else:
        gray_frame = resized_frame
    normalized = gray_frame / 255.0
    ascii_frame = ""
    for row in normalized:
        for pixel in row:
            index = int(pixel * (len(ascii_chars) - 1))
            ascii_frame += ascii_chars[index]
        ascii_frame += "\n"
    return ascii_frame


def play_video_in_terminal(video_path, width=80, fps=30):
    if not os.path.exists(video_path):
        print(f"Error: Video file '{video_path}' not found.")
        return
    cap = cv2.VideoCapture(video_path)
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_delay = 1.0 / video_fps if video_fps > 0 else (1.0 / fps if fps > 0 else 1.0 / 30)
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            ascii_art = convert_frame_to_ascii(frame, width)
            os.system('cls' if os.name == 'nt' else 'clear')
            print(ascii_art)
            time.sleep(frame_delay)
    except KeyboardInterrupt:
        print("\nVideo playback interrupted.")
    finally:
        cap.release()


def play_webcam_in_terminal(width=80, fps=30):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not access webcam.")
        return
    frame_delay = 1.0 / fps if fps > 0 else 1.0 / 30
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            ascii_art = convert_frame_to_ascii(frame, width)
            os.system('cls' if os.name == 'nt' else 'clear')
            print(ascii_art)
            time.sleep(frame_delay)
    except KeyboardInterrupt:
        print("\nWebcam playback interrupted.")
    finally:
        cap.release()


if __name__ == "__main__":
    print("1. Play video file (auto from Downloads)")
    print("2. Play webcam")
    choice = input("Choose option (1/2): ").strip()

    width = 100   # default ASCII width
    fps = 30      # default FPS

    if choice == "1":
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        video_path = os.path.join(downloads_folder, "vid.mp4")  # Auto-load vid.mp4
        play_video_in_terminal(video_path, width, fps)
    elif choice == "2":
        play_webcam_in_terminal(width, fps)
    else:
        print("Invalid choice.")
