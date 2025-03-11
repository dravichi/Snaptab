import os
import sys
import json
import pkg_resources

# List of Poppler executables you need to check for
POPPLER_EXECUTABLES = ['pdftoppm.exe', 'pdftocairo.exe']
CONFIG_FILE = os.path.join(os.path.expanduser("~"), '.poppler_config.json')  # Store in the user's home directory

# Function to get the Poppler path
def get_poppler_path():
    """
    Retrieves the Poppler path. If the path is already stored, use it.
    Otherwise, prompt the user to enter the Poppler path and store it for future use.
    """
    # Try loading the Poppler path from the configuration file
    stored_poppler_path = load_poppler_path()

    if stored_poppler_path:
        print(f"Using stored Poppler path: {stored_poppler_path}")
        try:
            return check_poppler_path(stored_poppler_path)  # Verifies path
        except ValueError as e:
            print(f"Error: {e}")
    
    # If no stored path, ask the user for input
    user_poppler_path = input("Poppler not found. Please provide the path to Poppler: ").strip()
    
    if user_poppler_path:
        try:
            # Validate the user input and check if the path is correct
            valid_poppler_path = check_poppler_path(user_poppler_path, is_user_input=True)  # Only print if user input
            save_poppler_path(valid_poppler_path)  # Save the valid path for future use
            return valid_poppler_path
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)
    
    raise ValueError("Poppler path not found. Exiting...")

# Set Poppler path (for internal use)
def set_poppler_path(user_poppler_path):
    """
    Sets the Poppler path for internal usage after validation.
    """
    # Validate the provided Poppler path
    valid_poppler_path = check_poppler_path(user_poppler_path, is_user_input=True)
    os.environ["POPPLER_PATH"] = valid_poppler_path  # Store in the environment
    print(f"Poppler path set to: {valid_poppler_path}")

# Check Poppler path
def check_poppler_path(poppler_path, is_user_input=False):
    """
    Verifies if the given Poppler path is valid by checking the existence of
    necessary Poppler executables (e.g., pdftoppm, pdftocairo).
    
    Parameters:
        poppler_path (str): Path to the Poppler directory.
        is_user_input (bool): Flag to print messages only if the path is from user input.
    """
    if is_user_input:
        print(f"Checking Poppler path: {poppler_path}")
    
    # Check if the provided Poppler path exists
    if not os.path.exists(poppler_path):
        raise ValueError(f"Poppler path does not exist: {poppler_path}")
    
    # Check if Poppler executables exist in the provided path
    missing_executables = []
    for exe in POPPLER_EXECUTABLES:
        exe_path = os.path.join(poppler_path, exe)
        if not os.path.isfile(exe_path):
            missing_executables.append(exe)
    
    if missing_executables:
        raise ValueError(f"Missing Poppler executables: {', '.join(missing_executables)}")

    # If all checks pass, return the valid Poppler path
    if is_user_input:
        print(f"Poppler path is valid: {poppler_path}")
    return poppler_path

# Save Poppler path to config
def save_poppler_path(poppler_path):
    """
    Saves the Poppler path to a configuration file.
    """
    config_data = {"poppler_path": poppler_path}
    with open(CONFIG_FILE, 'w') as config_file:
        json.dump(config_data, config_file)
    print(f"Poppler path saved to {CONFIG_FILE}")

# Load Poppler path from config
def load_poppler_path():
    """
    Loads the Poppler path from the configuration file if it exists.
    """
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as config_file:
            config_data = json.load(config_file)
            return config_data.get("poppler_path")
    return None

# Get the model path
def get_model_path():
    """
    Retrieves the path of the model file bundled with the package.
    Uses pkg_resources to access the model inside the package.
    """
    # This will resolve the model path relative to the installed package
    model_path = pkg_resources.resource_filename('snaptab', 'model/snaptab.pt')
    
    # Check if the model file exists in the packaged directory
    if not os.path.exists(model_path):
        raise ValueError(f"Model file not found: {model_path}")
    
    return model_path