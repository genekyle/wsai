import random
import time

def random_sleep(min_duration, max_duration):
    sleep_duration = random.uniform(min_duration, max_duration)
    print(f"Randomly Sleeping For {sleep_duration} Seconds...")
    time.sleep(sleep_duration)
    