#This script extracts cache data from various web browsers on Windows, macOS, and Linux platforms. 
#It dynamically determines the correct cache folder paths based on the operating system and browser used. 
#The script then walks through the cache directories to list all cached files and saves the results in a text file for each browser. 
#If the cache path doesn't exist or is empty, it returns an error message.
import os
import platform
import shutil
import getpass

def get_browser_cache_path(browser):
    user_profile = getpass.getuser()
    
    if platform.system() == 'Windows':
        if browser in ['chrome', 'brave']:
            cache_path = os.path.join(
                "C:\\Users", user_profile, "AppData", "Local", "BraveSoftware", "Brave-Browser", "User Data", "Default", "Cache"
            )
            if not os.path.exists(cache_path):
                cache_path = os.path.join(
                    "C:\\Users", user_profile, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Cache"
                )
            return cache_path
        elif browser == 'edge':
            return os.path.join(
                "C:\\Users", user_profile, "AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "Cache"
            )
    elif platform.system() == 'Darwin':  # macOS
        if browser in ['chrome', 'brave']:
            return os.path.join(
                "/Users", user_profile, "Library", "Application Support", "BraveSoftware", "Brave-Browser", "User Data", "Default", "Cache"
            )
        elif browser == 'edge':
            return os.path.join(
                "/Users", user_profile, "Library", "Application Support", "Microsoft", "Edge", "User Data", "Default", "Cache"
            )
    elif platform.system() == 'Linux':  # Linux
        if browser in ['chrome', 'brave']:
            return os.path.join(
                "/home", user_profile, ".config", "brave-browser", "User Data", "Default", "Cache"
            )
        elif browser == 'edge':
            return os.path.join(
                "/home", user_profile, ".config", "microsoft-edge", "User Data", "Default", "Cache"
            )
        elif browser == 'firefox':  # For Firefox on Linux
            return os.path.join(
                "/home", user_profile, ".mozilla", "firefox", "profile.default", "cache2"
            )
    elif platform.system() == 'Windows':  # For Firefox on Windows
        if browser == 'firefox':
            return os.path.join(
                "C:\\Users", user_profile, "AppData", "Local", "Mozilla", "Firefox", "Profiles", "profile.default", "cache2"
            )
    else:
        raise Exception(f"Unsupported browser or platform: {browser}")

def extract_cache_data(browser):
    cache_path = get_browser_cache_path(browser)
    if not cache_path or not os.path.exists(cache_path):
        print(f"Error: The cache path for {browser} does not exist at {cache_path}")
        return None
    
    # List cache files in the cache directory
    cached_files = []
    for root, dirs, files in os.walk(cache_path):
        for file in files:
            cached_files.append(os.path.join(root, file))
    
    if not cached_files:
        print(f"No cached files found for {browser}.")
        return None
    
    return cached_files

def extract_cache_from_all_browsers():
    browsers = ['chrome', 'brave', 'firefox', 'edge']
    all_cache_data = {}
    for browser in browsers:
        print(f"Extracting cache from {browser}...")
        cache_data = extract_cache_data(browser)
        if cache_data:
            all_cache_data[browser] = cache_data
            # Optionally, save the list of cache files to a text file
            with open(f"{browser}_cache.txt", "w") as file:
                for cache_file in cache_data:
                    file.write(f"{cache_file}\n")
    if all_cache_data:
        print(f"Cache data has been saved for all browsers.")

# Run the function to extract cache data from all browsers
extract_cache_from_all_browsers()
