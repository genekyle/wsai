def navigate_to(session_manager, session_id, url):
    driver = session_manager.get_browser_session(session_id)
    driver.get(url)
