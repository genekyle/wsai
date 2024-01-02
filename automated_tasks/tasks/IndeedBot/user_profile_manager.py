import json
import os

def get_profiles_file_path():
    # Assuming this script is located in root(wsai)/automated_tasks/tasks/IndeedBot/
    # Adjust the path accordingly if the script's location is different
    base_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(base_dir, "UserProfiles", "profiles.json")

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
