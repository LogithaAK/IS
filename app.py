from flask import Flask, render_template, request, redirect, url_for
from cryptography.fernet import Fernet
import os

app = Flask(__name__)
messages = []
shift_value = 3  # Default Caesar cipher shift

# Load or generate Fernet key
if not os.path.exists("secret.key"):
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
else:
    with open("secret.key", "rb") as key_file:
        key = key_file.read()

cipher = Fernet(key)

# Caesar Cipher functions
def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            result += chr((ord(char) + shift - offset) % 26 + offset)
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

@app.route("/", methods=["GET", "POST"])
def index():
    global shift_value
    if request.method == "POST":
        shift_value = int(request.form.get("shift", 3))
        message = request.form.get("message")
        encrypted_caesar = caesar_encrypt(message, shift_value)
        encrypted_message = cipher.encrypt(encrypted_caesar.encode()).decode()
        messages.append(encrypted_message)
        return redirect(url_for('index'))

    decrypted_messages = []
    for m in messages:
        decrypted_text = cipher.decrypt(m.encode()).decode()
        original_text = caesar_decrypt(decrypted_text, shift_value)
        decrypted_messages.append((original_text, decrypted_text, m))

    return render_template("index.html", messages=decrypted_messages, shift=shift_value)

if __name__ == "__main__":
    app.run(debug=True)
