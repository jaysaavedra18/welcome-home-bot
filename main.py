from camera import capture_image
from recognition import recognize_person
from notifications import send_notification
from profiles import load_profiles, add_profile

def main():
    # Load profiles
    profiles = load_profiles()

    # Capture image from camera
    image = capture_image()

    # Identify person
    person, height = recognize_person(image, profiles)

    if person:
        print(f"Recognized: {person['name']}")
        # send_notification(person['name'], person['phone'])
    else:
        print("Unrecognized person detected!")
        new_profile = add_profile(height)
        profiles.append(new_profile)
        # You can also send a notification for unrecognized person

if __name__ == "__main__":
    main()
