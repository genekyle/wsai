class IndeedBotStateManager:
    def __init__(self):
        self.current_state = "Not Started"

    def update_state(self, new_state):
        self.current_state = new_state
        print(f"State updated to: {self.current_state}")  # For demonstration purposes
