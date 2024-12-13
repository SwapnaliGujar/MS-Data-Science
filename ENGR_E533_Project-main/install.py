import subprocess
import os

def install():
    print("Creating virtual environment...")
    
    # Define the command to create a virtual environment
    if os.name == 'nt':  
        print('environment windows')
        subprocess.call(r"py -m venv .venv", shell=True)
        venv_activate_command = r".venv\Scripts\activate && "
    else:  # macOS/Linux
        print('environment linux or macos')
        subprocess.call(r"python3 -m venv .venv", shell=True)
        venv_activate_command = r"source .venv/bin/activate && "
    
    print("Installing dependencies...")
    
    # Use pip to install a specific version of a package
    install_command = "pip install uv==0.4.7"
    subprocess.call(venv_activate_command + install_command, shell=True)
    
    install_command = "pip install -e ."
    result = subprocess.call(venv_activate_command + install_command, shell=True)
    
    if result == 0:
        print("\n\n-----Installation Complete!-----")
    else:
        raise Exception("\n\n-----Failure during installation!-----")

if __name__ == "__main__":
    install()