import json
import os

def get_profiles_file_path():
    return os.path.join("IndeedBot", "UserProfiles", "profiles.json")

def load_user_profiles():
    profiles_file_path = get_profiles_file_path()
    if not os.path.exists(profiles_file_path):
        return []

    with open(profiles_file_path, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def save_user_profile(profile):
    profiles = load_user_profiles()
    profiles.append(profile)
    with open(get_profiles_file_path(), "w") as file:
        json.dump(profiles, file, indent=4)
