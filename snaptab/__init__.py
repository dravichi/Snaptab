import os
import sys
import json
import pkg_resources

POPPLER_EXECUTABLES = ['pdftoppm.exe', 'pdftocairo.exe']
CONFIG_FILE = os.path.join(os.path.expanduser("~"), '.poppler_config.json')

def get_poppler_path():
    stored_poppler_path = load_poppler_path()
    if stored_poppler_path:
        print(f"Using stored Poppler path: {stored_poppler_path}")
        try:
            return check_poppler_path(stored_poppler_path)
        except ValueError as e:
            print(f"Error: {e}")
    
    user_poppler_path = input("Poppler not found. Please provide the path to Poppler: ").strip()
    
    if user_poppler_path:
        try:
            valid_poppler_path = check_poppler_path(user_poppler_path, is_user_input=True)
            save_poppler_path(valid_poppler_path)
            return valid_poppler_path
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)
    raise ValueError("Poppler path not found. Exiting...")

def set_poppler_path(user_poppler_path):
    valid_poppler_path = check_poppler_path(user_poppler_path, is_user_input=True)
    os.environ["POPPLER_PATH"] = valid_poppler_path  
    print(f"Poppler path set to: {valid_poppler_path}")

def check_poppler_path(poppler_path, is_user_input=False):
    if is_user_input:
        print(f"Checking Poppler path: {poppler_path}")
    
    if not os.path.exists(poppler_path):
        raise ValueError(f"Poppler path does not exist: {poppler_path}")
    
    missing_executables = []
    for exe in POPPLER_EXECUTABLES:
        exe_path = os.path.join(poppler_path, exe)
        if not os.path.isfile(exe_path):
            missing_executables.append(exe)
    
    if missing_executables:
        raise ValueError(f"Missing Poppler executables: {', '.join(missing_executables)}")

    return poppler_path

def save_poppler_path(poppler_path):
    config_data = {"poppler_path": poppler_path}
    with open(CONFIG_FILE, 'w') as config_file:
        json.dump(config_data, config_file)
    print(f"Poppler path saved to {CONFIG_FILE}")

def load_poppler_path():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as config_file:
            config_data = json.load(config_file)
            return config_data.get("poppler_path")
    return None

def get_model_path():
    model_path = pkg_resources.resource_filename('snaptab', 'model/snaptab.pt')
    
    if not os.path.exists(model_path):
        raise ValueError(f"Model file not found: {model_path}")
    
    return model_path