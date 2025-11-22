import cv2
import time

# ================= CONFIGURATION =================
# Change this to 4 if testing your specific USB port, or 0 for default webcam
CAMERA_INDEX = 4  
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
# =================================================

def test_camera():
    # Initialize VideoCapture with V4L2 backend (recommended for Linux)
    cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_V4L2)

    # 1. Force MJPG Compression (Crucial for fixing timeouts on USB 2.0)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

    # 2. Set Resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    # Check if camera opened successfully
    if not cap.isOpened():
        print(f"ERROR: Could not open camera index {CAMERA_INDEX}.")
        print("Check connection or try a different index (0, 1, 2, etc).")
        return

    # Print actual resolution set by the camera
    actual_w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    actual_h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"Camera opened: {int(actual_w)}x{int(actual_h)}")
    print("Press 'q' to exit.")

    # Create a resizable window
    cv2.namedWindow('Camera Test', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Camera Test', 960, 540) # Display at manageable size

    prev_time = 0
    
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to grab frame.")
            break

        # Calculate FPS
        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time

        # Draw FPS on frame
        cv2.putText(frame, f"FPS: {int(fps)}", (20, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Camera Test', frame)

        # Press 'q' to quit
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_camera()