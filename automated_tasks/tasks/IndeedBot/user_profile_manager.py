import json
import os

def load_user_profiles():
    try:
        with open("IndeedBot/UserProfiles/profiles.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_user_profile(profile):
    profiles = load_user_profiles()
    profiles.append(profile)
    with open("IndeedBot/UserProfiles/profiles.json", "w") as file:
        json.dump(profiles, file, indent=4)
