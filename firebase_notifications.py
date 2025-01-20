from typing import Dict, Optional
from datetime import datetime, timedelta
import os
import firebase_admin
from firebase_admin import credentials, messaging
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

class FirebaseNotificationSystem:
    def __init__(self, cred_path: Optional[str] = None):
        """Initialize the Firebase notification system."""
        if not firebase_admin._apps:
            cred_path = cred_path or os.getenv('FIREBASE_CREDENTIAL_PATH')
            if not cred_path:
                raise ValueError(
                    "Firebase credentials path must be provided either as an argument "
                    "or through FIREBASE_CREDENTIAL_PATH environment variable"
                )
            
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        
        self.household_members: Dict[str, str] = {}  # name -> FCM token
        self.notification_history: Dict[str, datetime] = {}  # name -> last notification time
        self.cooldown_period = timedelta(minutes=0)  # Prevent spam notifications
    
    def add_household_member(self, name: str, fcm_token: str) -> None:
        """Add or update a household member's FCM token."""
        logger.debug(f"Adding household member: {name} with token: {fcm_token[:20]}...")
        self.household_members[name.lower()] = fcm_token
    
    def _should_notify(self, name: str) -> bool:
        """Check if enough time has passed since the last notification."""
        if name not in self.notification_history:
            return True
            
        time_since_last = datetime.now() - self.notification_history[name]
        return time_since_last > self.cooldown_period
    
    def send_notification(self, token: str, title: str, body: str) -> None:
        """Send a notification to a specific token."""
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                token=token
            )
            response = messaging.send(message)
            logger.debug(f"Notification sent successfully: {response}")
        except Exception as e:
            logger.error(f"Failed to send notification: {str(e)}")
            raise
    
    def notify_household(self, title: str, body: str, exclude_name: Optional[str] = None) -> None:
        """Send a notification to all household members except the one specified."""
        exclude_name = exclude_name.lower() if exclude_name else None
        
        for name, token in self.household_members.items():
            if name != exclude_name:
                try:
                    self.send_notification(token, title, body)
                except Exception as e:
                    logger.error(f"Failed to send notification to {name}: {str(e)}")

    def handle_person_detected(self, name: str, is_known: bool = True) -> None:
        """Handle person detection event and send appropriate notifications."""
        name_lower = name.lower()
        current_time = datetime.now()
        
        logger.debug(f"Handling {'known' if is_known else 'unknown'} person detection: {name}")
        
        # Check cooldown period
        if not self._should_notify(name_lower):
            logger.debug(f"Skipping notification due to cooldown for: {name}")
            return
            
        self.notification_history[name_lower] = current_time
        
        if is_known:
            # First, send a personal welcome notification to the detected person
            if name_lower in self.household_members:
                try:
                    personal_token = self.household_members[name_lower]
                    self.send_notification(
                        personal_token,
                        "Welcome Home!",
                        f"Welcome back, {name}!"
                    )
                    logger.debug(f"Sent welcome notification to {name}")
                except Exception as e:
                    logger.error(f"Failed to send welcome notification to {name}: {str(e)}")
            
            # Then notify others about their arrival
            title = "Household Update"
            body = f"{name} has arrived home."
            self.notify_household(title, body, exclude_name=name)
            
        else:
            # Unknown person detected - notify everyone
            title = "⚠️ Security Alert"
            body = "Unknown person detected at the entrance"
            self.notify_household(title, body)

def create_notification_system(cred_path: Optional[str] = None) -> FirebaseNotificationSystem:
    """Create a notification system instance."""
    return FirebaseNotificationSystem(cred_path)