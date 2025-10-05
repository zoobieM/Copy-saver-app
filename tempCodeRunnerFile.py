
            os.system('cls' if os.name == 'nt' else 'clear')
            print(ascii_art)

            time.sleep(frame_delay)

    except KeyboardInterrupt:
        print("\nVideo playback interrupted.")

    finally:
        cap.release()


def play_webcam_in_terminal(width=80, fps=30):
    """
    Play webcam feed in the terminal using ASCII characters
    """
    cap = cv2.VideoCapture(0)  # 0 = default webcam
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
    print("1. Play video file")
    print("2. Play webcam")
    choice = input("Choose option (1/2): ").strip()

    try:
        width = int(input("Enter terminal width (default 80): ") or "80")