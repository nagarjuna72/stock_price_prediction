import os
import json
import re

# Path to the JSON file storing user data
USER_DATA_FILE = "user_data.json"

# Load user data from JSON file
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    return {}

# Save user data to JSON file
def save_user_data(user_data):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(user_data, file, indent=4)

# Validation functions
def is_valid_username(username):
    if not username:
        return False, "Username is required."
    if username[0].isdigit():
        return False, "Username must not start with a digit."
    if len(username) < 6:
        return False, "Username must be at least 6 characters long."
    return True, ""

def is_valid_password(password):
    if not password:
        return False, "Password is required."
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character."
    return True, ""

# Authentication functions
def login(username, password, user_data):
    if username in user_data and user_data[username] == password:
        return True
    return False

def signup(username, password, user_data):
    if username in user_data:
        return False  # Username already exists
    user_data[username] = password
    save_user_data(user_data)  # Save new user data
    return True
