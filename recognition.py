import face_recognition
import cv2
import numpy as np
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import threading
import time

class FaceRecognitionSystem:
    def __init__(self, known_faces_dir: str = "known_faces", 
                 notification_callback=None):
        """
        Initialize the face recognition system.
        
        Args:
            known_faces_dir: Directory containing known face images
            notification_callback: Function to handle notifications
        """
        self.known_faces_dir = known_faces_dir
        self.known_face_encodings = []
        self.known_face_names = []
        self.notification_callback = notification_callback
        self.last_notification_time = {}  # Prevent spam notifications
        self.notification_cooldown = 60  # seconds
        
        # Create known_faces directory if it doesn't exist
        if not os.path.exists(known_faces_dir):
            os.makedirs(known_faces_dir)
            
        self.load_known_faces()
    
    def load_known_faces(self):
        """Load all known faces from the known_faces directory."""
        self.known_face_encodings = []
        self.known_face_names = []
        
        for filename in os.listdir(self.known_faces_dir):
            if filename.endswith((".jpg", ".jpeg", ".png")):
                path = os.path.join(self.known_faces_dir, filename)
                name = os.path.splitext(filename)[0]
                
                image = face_recognition.load_image_file(path)
                face_encodings = face_recognition.face_encodings(image)
                
                if face_encodings:
                    self.known_face_encodings.append(face_encodings[0])
                    self.known_face_names.append(name)
    
    def add_new_face(self, frame, name: str) -> bool:
        """
        Add a new face to the known faces directory.
        
        Args:
            frame: Video frame containing the face
            name: Name of the person
        
        Returns:
            bool: True if face was successfully added
        """
        face_locations = face_recognition.face_locations(frame)
        if not face_locations:
            return False
            
        # Save the face image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.jpg"
        path = os.path.join(self.known_faces_dir, filename)
        
        # Crop and save just the face region
        top, right, bottom, left = face_locations[0]
        face_image = frame[top:bottom, left:right]
        cv2.imwrite(path, cv2.cvtColor(face_image, cv2.COLOR_RGB2BGR))
        
        # Update known faces
        face_encoding = face_recognition.face_encodings(frame, face_locations)[0]
        self.known_face_encodings.append(face_encoding)
        self.known_face_names.append(name)
        
        return True
    
    def process_frame(self, frame) -> Tuple[List[str], List[tuple]]:
        """
        Process a video frame for face recognition.
        
        Args:
            frame: Video frame to process
            
        Returns:
            Tuple containing:
            - List of names of recognized people
            - List of face locations (top, right, bottom, left)
        """
        # Convert frame from BGR (OpenCV) to RGB (face_recognition)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Find all faces in the frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        face_names = []
        
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(
                self.known_face_encodings, 
                face_encoding,
                tolerance=0.6
            )
            name = "Unknown"
            
            if True in matches:
                first_match_index = matches.index(True)
                name = self.known_face_names[first_match_index]
            
            face_names.append(name)
            
            # Send notification if enough time has passed
            current_time = time.time()
            if (name not in self.last_notification_time or 
                current_time - self.last_notification_time.get(name, 0) > self.notification_cooldown):
                
                if self.notification_callback:
                    if name == "Unknown":
                        self.notification_callback(
                            "Unknown person detected! Please check security feed."
                        )
                    else:
                        self.notification_callback(f"Welcome home {name}!")
                        
                self.last_notification_time[name] = current_time
        
        return face_names, face_locations
    
    def draw_results(self, frame, face_locations: List[tuple], face_names: List[str]):
        """
        Draw boxes and labels for recognized faces on the frame.
        
        Args:
            frame: Video frame to draw on
            face_locations: List of face location tuples
            face_names: List of names corresponding to the faces
        """
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            
            # Draw a label with the name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.6, (255, 255, 255), 1)