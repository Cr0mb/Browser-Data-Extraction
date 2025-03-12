# Browser-Data-Extraction
This repository contains a set of Python scripts designed to extract browser data such as history, bookmarks, cookies, passwords, cache, and download history from popular browsers like Chrome, Brave, Edge, Firefox, and Opera. The scripts are cross-platform and work on Windows, macOS, and Linux.


## Overview
The repository includes three major components:

- Browser History Extractor: Extracts browsing history from supported browsers and saves it as a CSV file.
- Bookmarks Extractor: Extracts bookmarks from supported browsers and saves them as CSV files.
- Cookies Extractor: Extracts cookies from supported browsers and saves them in an SQLite database.
- Password Extraction: Extracts and decrypts saved passwords from supported browsers.
- Cache Extraction: Extracts cached files from supported browsers.
- Download History Extraction: Extracts the download history from supported browsers.

## Install
```
pip install pandas psutil pycryptodome colorama pywin32
```


1. Browser History Extractor
The Browser History Extractor fetches browsing history from supported browsers (Chrome, Brave, Edge, Firefox) and saves it to a CSV file.
-This will generate CSV files for each browser (chrome_history.csv, brave_history.csv, edge_history.csv, firefox_history.csv) and a combined file (combined_history.csv).

2. Bookmarks Extractor
The Bookmarks Extractor fetches bookmarks from supported browsers (Chrome, Brave, Edge) and saves them in CSV format.
- This will create CSV files for each browser's bookmarks (chrome_bookmarks.csv, brave_bookmarks.csv, edge_bookmarks.csv).

3. Cookies Extractor
The Cookies Extractor extracts cookies from the supported browsers (Chrome, Brave, Edge). If the browser is running, it will automatically be closed to prevent conflicts.
- This will extract the cookies and store them in a temporary SQLite database file.

4. Password Extraction Script
This script extracts and decrypts saved passwords from supported browsers (Chrome, Firefox, Brave, Edge, Opera).
- This will generate a CSV file, decrypted_password.csv, containing browser, URL, username, password, and the current user's name.

5. Cache Extraction Script
This script extracts cached files from supported browsers (Chrome, Brave, Firefox, Edge).
- This will generate text files (e.g., chrome_cache.txt, brave_cache.txt) containing paths to cached files.

6. Download History Extraction Script (download_history_extractor.py)
This script extracts download history from supported browsers (Chrome, Brave, Edge, Firefox).
- This will output the download history, including download IDs, file paths, and timestamps.

## Features
> Cross-platform: Supports Windows, macOS, and Linux.

> Automatic Browser Closure: Automatically closes the browser before extracting cookies to prevent conflicts.

> CSV Output: Extracted data (history, bookmarks, and passwords) is saved in CSV format for easy access.

> SQLite Database: Cookies are saved in an SQLite database, making them easy to query.

> Password Decryption: Retrieves and decrypts saved passwords from supported browsers.

## Security and Ethical Considerations
These scripts are intended solely for educational purposes to understand how browsers store and manage sensitive data.

Please use them responsibly and always with permission. 

Unauthorized access to others' data is illegal and unethical.

Ensure that you have explicit permission to access and use the data from browsers.



