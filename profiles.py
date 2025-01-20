import json

def load_profiles():
    try:
        with open('profiles.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def add_profile(height):
    name = input("Enter name: ")
    phone = input("Enter phone number: ")
    
    new_profile = {"name": name, "height": height, "phone": phone}
    
    # Optionally save the new profile to a file
    profiles = load_profiles()
    profiles.append(new_profile)
    with open('profiles.json', 'w') as f:
        json.dump(profiles, f)
    
    return new_profile
