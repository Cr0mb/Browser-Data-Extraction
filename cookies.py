#This script extracts cookies from three major web browsers (Chrome, Brave, and Edge) on various platforms (Windows, macOS, Linux). 
#It identifies the location of the browser's cookie database, checks if the browser is running, and closes it automatically if necessary. 
#It then copies the cookies database to a temporary file, extracts cookie data using SQLite, and stores it in a DataFrame. 
#The extracted cookie information includes details like host, name, value, path, expiration, secure flag, and HTTPOnly flag. 
#The script saves the cookies in CSV files for each browser. It ensures the browser is not running while accessing the cookies to avoid file access conflicts.
import os
import shutil
import sqlite3
import platform
import pandas as pd
import getpass
import psutil
import subprocess

def get_cookies_path(browser):
    user_profile = getpass.getuser()
    if platform.system() == 'Windows':
        if browser == 'brave' or browser == 'chrome':
            cookies_path = os.path.join(
                "C:\\Users", user_profile, "AppData", "Local", "BraveSoftware", "Brave-Browser", "User Data", "Default", "Network", "Cookies"
            )
            if not os.path.exists(cookies_path):
                cookies_path = os.path.join(
                    "C:\\Users", user_profile, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Network", "Cookies"
                )
            return cookies_path
        elif browser == 'edge':
            return os.path.join(
                "C:\\Users", user_profile, "AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "Network", "Cookies"
            )
    elif platform.system() == 'Darwin':  # macOS
        if browser == 'brave':
            return os.path.join("/Users", user_profile, "Library", "Application Support", "BraveSoftware", "Brave-Browser", "User Data", "Default", "Network", "Cookies")
        elif browser == 'chrome':
            return os.path.join("/Users", user_profile, "Library", "Application Support", "Google", "Chrome", "User Data", "Default", "Network", "Cookies")
        elif browser == 'edge':
            return os.path.join("/Users", user_profile, "Library", "Application Support", "Microsoft Edge", "User Data", "Default", "Network", "Cookies")
    elif platform.system() == 'Linux':  # Linux
        if browser == 'brave':
            return os.path.join("/home", user_profile, ".config", "BraveSoftware", "Brave-Browser", "User Data", "Default", "Network", "Cookies")
        elif browser == 'chrome':
            return os.path.join("/home", user_profile, ".config", "google-chrome", "User Data", "Default", "Network", "Cookies")
        elif browser == 'edge':
            return os.path.join("/home", user_profile, ".config", "microsoft-edge", "User Data", "Default", "Network", "Cookies")
    return None

def is_browser_running(browser):
    """Check if the browser is running."""
    for process in psutil.process_iter(attrs=['name']):
        if browser.lower() in process.info['name'].lower():
            return True
    return False

def close_browser(browser):
    """Close the browser if it's running."""
    print(f"Automatically closing {browser}...")
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if browser.lower() in process.info['name'].lower():
            subprocess.call(["taskkill", "/F", "/PID", str(process.info['pid'])], shell=True)
            print(f"Closed {browser} (PID {process.info['pid']})")

def extract_cookies(browser):
    """Extract cookies from the specified browser."""
    cookies_path = get_cookies_path(browser)
    if not cookies_path or not os.path.exists(cookies_path):
        print(f"Error: The specified {browser} cookies file does not exist at {cookies_path}")
        return None
    
    if is_browser_running(browser):
        close_browser(browser)
    
    temp_cookies_path = "temp_cookies.db"
    try:
        shutil.copy2(cookies_path, temp_cookies_path)
    except PermissionError:
        print(f"Error: The {browser} cookies file is still in use by the browser.")
        return None

    conn = sqlite3.connect(temp_cookies_path)
    cursor = conn.cursor()
    query = """
    SELECT host_key, name, value, path, expires_utc, is_secure, is_httponly
    FROM cookies
    """
    cursor.execute(query)
    cookies_data = cursor.fetchall()
    df = pd.DataFrame(cookies_data, columns=['Host', 'Name', 'Value', 'Path', 'Expires', 'Secure', 'HttpOnly'])
    conn.close()
    os.remove(temp_cookies_path)
    return df

def extract_cookies_from_all_browsers():
    """Extract cookies from all supported browsers."""
    browsers = ['chrome', 'brave', 'edge']
    for browser in browsers:
        print(f"Extracting cookies from {browser}...")
        df = extract_cookies(browser)
        if df is not None:
            df.to_csv(f"{browser}_cookies.csv", index=False)
            print(f"Cookies from {browser} saved to {browser}_cookies.csv")

df_combined = extract_cookies_from_all_browsers()
