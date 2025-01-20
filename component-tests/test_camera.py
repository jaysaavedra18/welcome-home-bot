import sys
import os

# Add the path to the camera module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from camera import capture_video

# Run the test for live video feed capture
def test_capture_video():
    print("Starting live video feed test. Press 'q' to exit the video window.")
    
    try:
        # Start capturing video
        capture_video()
    except Exception as e:
        print(f"An error occurred during video capture: {e}")

# Run the test
if __name__ == "__main__":
    test_capture_video()
