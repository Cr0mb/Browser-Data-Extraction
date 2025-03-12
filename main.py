import os
import sys
import pyfiglet

def run_script(script_name):
    try:
        os.system(f'python {script_name}')
    except Exception as e:
        print(f"Error running {script_name}: {e}")

def run_all_scripts():
    scripts = ["history.py", "bookmarks.py", "cookies.py", "passwords.py", "cache.py", "downloads.py"]
    for script in scripts:
        run_script(script)

def print_banner():
    banner = pyfiglet.figlet_format("BrowseX")
    print(banner)
    print("\n===============", "\nMade by Cr0mb", "\n===============")

def main_menu():
    print_banner()
    while True:
        print("\nSelect a script to run:")
        print("1. History")
        print("2. Bookmarks")
        print("3. Cookies")
        print("4. Passwords")
        print("5. Cache")
        print("6. Downloads")
        print("7. Run All Scripts")
        print("8. Exit")
        
        choice = input("\nEnter the number of your choice: ")

        if choice == '1':
            run_script("history.py")
        elif choice == '2':
            run_script("bookmarks.py")
        elif choice == '3':
            run_script("cookies.py")
        elif choice == '4':
            run_script("passwords.py")
        elif choice == '5':
            run_script("cache.py")
        elif choice == '6':
            run_script("downloads.py")
        elif choice == '7':
            run_all_scripts()
        elif choice == '8':
            print("\nExiting Hacker Mode...")
            sys.exit()
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
