from db.DatabaseManager import UserProfile, Session

def load_user_profiles():
    with Session() as session:
        return session.query(UserProfile).all()

def save_user_profile(profile_data):
    with Session() as session:
        new_profile = UserProfile(username=profile_data["username"], password=profile_data["password"])
        session.add(new_profile)
        session.commit()
