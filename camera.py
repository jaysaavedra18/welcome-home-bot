import cv2
from recognition import FaceRecognitionSystem
import queue
import time
from firebase_notifications import create_notification_system

class WelcomeHomeBot:
    def __init__(self):
        # Initialize notification system for SMS
        self.notification_system = create_notification_system()
        # Add household members (you'll need to add your actual household members)
        self.notification_system.add_household_member("Jason", "CLIENT_KEY")
        # Add more household members as needed
        
        self.face_system = FaceRecognitionSystem(
            known_faces_dir="known_faces",
            notification_callback=self.send_notification
        )
        self.message_queue = queue.Queue()
        self.current_message = ""
        self.message_start_time = 0
        self.message_duration = 3  # seconds
        self.registration_mode = False
        self.registration_name = ""
        
    def send_notification(self, message: str):
        """
        Handle system notifications.
        Prints all messages to console but only sends SMS for specific events.
        """
        # Always print the message and add to display queue
        print(f"NOTIFICATION: {message}")
        # self.message_queue.put(message)
        
        # Only send SMS for arrival events
        if "Welcome home" in message:
            # Extract name and send SMS notification
            name = message.replace("Welcome home ", "").replace("!", "").split("_")[0]
            self.notification_system.handle_person_detected(name, is_known=True)
        elif "Unknown person detected!" in message:
            # Send SMS for unknown person
            self.notification_system.handle_person_detected("Unknown", is_known=False)
        
    def update_display_message(self):
        """Update the current display message if needed."""
        current_time = time.time()
        
        if (self.current_message and 
            current_time - self.message_start_time > self.message_duration):
            self.current_message = ""
            
        if not self.current_message and not self.message_queue.empty():
            self.current_message = self.message_queue.get()
            self.message_start_time = current_time

    def draw_overlay(self, frame):
        """Draw status messages and instructions on the frame."""
        height, width = frame.shape[:2]
        
        # Draw current message at the top
        if self.current_message:
            cv2.rectangle(frame, (0, 0), (width, 40), (0, 0, 0), cv2.FILLED)
            cv2.putText(frame, self.current_message, (10, 30), 
                       cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1)
        
        # Draw registration mode interface or normal instructions
        if self.registration_mode:
            # Draw registration interface
            cv2.rectangle(frame, (0, height-90), (width, height), (0, 0, 0), cv2.FILLED)
            cv2.putText(frame, "Registration Mode", (10, height-70),
                       cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 1)
            cv2.putText(frame, f"Name: {self.registration_name}", (10, height-40),
                       cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1)
            cv2.putText(frame, "Enter to save | Esc to cancel", (10, height-10),
                       cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1)
        else:
            pass
            # # Draw normal instructions
            # cv2.rectangle(frame, (0, height-30), (width, height), (0, 0, 0), cv2.FILLED)
            # if "Unknown" in self.last_face_names:
            #     instructions = "Press 'R' to register unknown face | 'Q' to quit"
            # else:
            #     instructions = "Press 'Q' to quit"
            # cv2.putText(frame, instructions, (10, height-10),
            #            cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

    def capture_video(self):
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open camera.")
            return

        self.last_face_names = []
        window_name = 'Welcome Home Bot'
        cv2.namedWindow(window_name)

        while True:
            ret, frame = cap.read()

            if not ret:
                print("Error: Could not read frame.")
                break

            # Process the frame for face recognition
            face_names, face_locations = self.face_system.process_frame(frame)
            self.last_face_names = face_names
            
            # Draw boxes and labels on the frame
            self.face_system.draw_results(frame, face_locations, face_names)
            
            # Update and draw the overlay
            self.update_display_message()
            self.draw_overlay(frame)

            # Display the frame
            cv2.imshow(window_name, frame)

            # Handle key presses with longer wait time
            key = cv2.waitKey(50) & 0xFF
            
            if self.registration_mode:
                if key == 27:  # ESC
                    self.registration_mode = False
                    self.registration_name = ""
                    self.send_notification("Registration cancelled")
                elif key == 13:  # Enter
                    if self.registration_name:
                        success = self.face_system.add_new_face(frame.copy(), self.registration_name)
                        if success:
                            self.send_notification(f"Successfully registered {self.registration_name}!")
                        else:
                            self.send_notification("No face detected in frame. Please try again.")
                        self.registration_mode = False
                        self.registration_name = ""
                elif key == 8:  # Backspace
                    self.registration_name = self.registration_name[:-1]
                elif 32 <= key <= 126:  # Printable characters
                    self.registration_name += chr(key)
            else:
                if key == ord('q'):
                    break
                elif key == ord('r') and "Unknown" in face_names:
                    self.registration_mode = True
                    self.send_notification("Enter name for unknown face")

        cap.release()
        cv2.destroyAllWindows()

def main():
    bot = WelcomeHomeBot()
    bot.capture_video()

if __name__ == "__main__":
    main()