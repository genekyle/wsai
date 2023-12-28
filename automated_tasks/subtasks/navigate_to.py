def navigate_to(session_manager, session_id, url):
    print(f"navigatin to {url}...")
    try:
        # Retrieve the WebDriver session
        driver = session_manager.get_browser_session(session_id)
        if not driver:
            print(f"Error: No valid WebDriver session found for session ID: {session_id}")
            return  # Exit the function if no valid session is found

        # Navigate to the URL
        driver.get(url)
        print(f"Navigated to {url} using session ID: {session_id}")  # Confirm navigation

    except Exception as e:
        # Log any exceptions that occur during navigation
        print(f"An error occurred while navigating to {url}: {e}")
