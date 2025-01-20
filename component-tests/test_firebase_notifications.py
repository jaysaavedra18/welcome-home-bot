import sys
import os
import time
import logging
from datetime import datetime

# Add the path to the camera module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from firebase_notifications import create_notification_system

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_notification_delivery():
    """
    Enhanced test script for Firebase notifications with better error handling
    and delivery confirmation logging.
    """
    notification_system = create_notification_system()
    logger.info("Notification system initialized")
    
    # Test FCM token validation
    test_token = "cjhZDYhpeMF2EIhPwsDnIN:APA91bFRyJUUIIUGWk2x990Q3YU5NAFU4THv96mvZqXJAp6dvO5RRMUlIwPBgvBldORW80N5LOfGmf4k4-cMiq1UTh7N_V9ld0085RMmo8Wi-eyB8Hgv0Ic"
    
    try:
        # Test token registration
        logger.info("Testing token registration...")
        notification_system.add_household_member("Jason", test_token)
        
        # Test 1: Known person detection with delivery confirmation
        logger.info("Test 1: Sending known person notification...")
        response = notification_system.handle_person_detected("Jason", is_known=True)
        logger.debug(f"Known person notification response: {response}")
        time.sleep(2)
        
        # Test 2: Unknown person detection with delivery confirmation
        logger.info("Test 2: Sending unknown person notification...")
        response = notification_system.handle_person_detected("Unknown", is_known=False)
        logger.debug(f"Unknown person notification response: {response}")
        time.sleep(2)
        
        # Test 3: Rapid succession test
        logger.info("Test 3: Testing rapid notifications...")
        for i in range(3):
            response = notification_system.handle_person_detected(
                "Jason" if i % 2 == 0 else "Unknown",
                is_known=(i % 2 == 0)
            )
            logger.debug(f"Rapid test {i+1} response: {response}")
            time.sleep(1)
            
        # Test 4: Token validation
        logger.info("Test 4: Verifying token validity...")
        if hasattr(notification_system, 'verify_token'):
            is_valid = notification_system.verify_token(test_token)
            logger.info(f"Token validation result: {is_valid}")
            
    except Exception as e:
        logger.error(f"Error during testing: {str(e)}", exc_info=True)
        return False
        
    return True

if __name__ == "__main__":
    print("Starting comprehensive notification testing...")
    success = test_notification_delivery()
    
    if success:
        print("\nTest completion checklist:")
        print("✓ 1. Verify both notifications appeared in the client")
        print("✓ 2. Check notification timestamps are correct")
        print("✓ 3. Confirm notification content is accurate")
        print("\nIf any checks failed, please verify:")
        print("- Firebase configuration is correct")
        print("- Client is subscribed to the correct topics")
        print("- FCM token is current and valid")
        print("- Network connectivity is stable")
        print("- Browser notifications are enabled")
        print("\nCheck the logs above for detailed debugging information")
    else:
        print("\nTesting failed. Please check the error logs above.")