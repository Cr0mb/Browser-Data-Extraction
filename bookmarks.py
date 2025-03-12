#This script extracts bookmarks from three popular web browsers on different platforms. 
#Script locates the browser's bookmark file, parses the JSON data to retrieve bookmark titles and URLs, and saves the extracted information in CSV format. 
#The script checks the existence of the bookmark file, reads and processes the JSON data, and stores the bookmarks found under the "bookmark_bar" and "other" sections. 
#It outputs individual CSV files for each browser's bookmarks.
import os
import json
import platform
import getpass
import pandas as pd

def get_bookmarks_path(browser):
    user_profile = getpass.getuser()
    if platform.system() == 'Windows':
        if browser == 'brave':
            return os.path.join("C:\\Users", user_profile, "AppData", "Local", "BraveSoftware", "Brave-Browser", "User Data", "Default", "Bookmarks")
        elif browser == 'chrome':
            return os.path.join("C:\\Users", user_profile, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Bookmarks")
        elif browser == 'edge':
            return os.path.join("C:\\Users", user_profile, "AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "Bookmarks")
    elif platform.system() == 'Darwin':  # macOS
        if browser == 'brave':
            return os.path.join("/Users", user_profile, "Library", "Application Support", "BraveSoftware", "Brave-Browser", "User Data", "Default", "Bookmarks")
        elif browser == 'chrome':
            return os.path.join("/Users", user_profile, "Library", "Application Support", "Google", "Chrome", "User Data", "Default", "Bookmarks")
        elif browser == 'edge':
            return os.path.join("/Users", user_profile, "Library", "Application Support", "Microsoft Edge", "User Data", "Default", "Bookmarks")
    elif platform.system() == 'Linux':  # Linux
        if browser == 'brave':
            return os.path.join("/home", user_profile, ".config", "BraveSoftware", "Brave-Browser", "User Data", "Default", "Bookmarks")
        elif browser == 'chrome':
            return os.path.join("/home", user_profile, ".config", "google-chrome", "User Data", "Default", "Bookmarks")
        elif browser == 'edge':
            return os.path.join("/home", user_profile, ".config", "microsoft-edge", "User Data", "Default", "Bookmarks")
    return None

def extract_bookmarks(browser):
    bookmarks_path = get_bookmarks_path(browser)
    if not bookmarks_path or not os.path.exists(bookmarks_path):
        print(f"Error: The specified {browser} bookmarks file does not exist at {bookmarks_path}")
        return None
    with open(bookmarks_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    def parse_bookmarks(bookmark_folder):
        bookmarks = []
        if "children" in bookmark_folder:
            for item in bookmark_folder["children"]:
                if "url" in item:
                    bookmarks.append((item["name"], item["url"]))
                elif "children" in item:
                    bookmarks.extend(parse_bookmarks(item))
        return bookmarks

    # Extract bookmarks from the 'bookmark_bar' and 'other' sections
    all_bookmarks = parse_bookmarks(data["roots"]["bookmark_bar"]) + parse_bookmarks(data["roots"]["other"])

    # Convert to DataFrame and save as CSV
    df = pd.DataFrame(all_bookmarks, columns=["Title", "URL"])
    df.to_csv(f"{browser}_bookmarks.csv", index=False)
    return df

def extract_bookmarks_from_all_browsers():
    browsers = ['chrome', 'brave', 'edge']
    for browser in browsers:
        print(f"Extracting bookmarks from {browser}...")
        df = extract_bookmarks(browser)
        if df is not None:
            print(f"Saved {browser} bookmarks to {browser}_bookmarks.csv")

extract_bookmarks_from_all_browsers()
