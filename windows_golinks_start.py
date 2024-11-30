#!/usr/bin/env python3
import os
import sys
import subprocess
import winreg
import ctypes
import venv
from pathlib import Path

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_command(cmd):
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(cmd)}: {e}")
        sys.exit(1)

def setup_venv():
    print("Setting up virtual environment...")
    if not os.path.exists("venv"):
        try:
            venv.create("venv", with_pip=True)
            # Install dependencies
            venv_pip = os.path.join("venv", "Scripts", "pip.exe")
            run_command([venv_pip, "install", "-r", "requirements.txt"])
            print("Virtual environment created and dependencies installed")
        except Exception as e:
            print(f"Error setting up virtual environment: {e}")
            sys.exit(1)
    else:
        print("Virtual environment already exists")

def setup_dns():
    print("Setting up DNS...")
    hosts_line = "127.0.0.1 go"
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    
    # Check if entry already exists
    with open(hosts_path, 'r') as f:
        if hosts_line in f.read():
            print("DNS entry already exists")
            return

    try:
        with open(hosts_path, 'a') as f:
            f.write(f"\n{hosts_line}\n")
        print("DNS entry added successfully")
    except Exception as e:
        print(f"Error setting up DNS: {e}")
        print("Please manually add '127.0.0.1 go' to %SystemRoot%\\System32\\drivers\\etc\\hosts")

def setup_nssm():
    print("Setting up NSSM service...")
    install_dir = os.path.abspath(os.path.dirname(__file__))
    venv_python = os.path.join(install_dir, "venv", "Scripts", "python.exe")
    app_path = os.path.join(install_dir, "app.py")
    
    # Check if NSSM is available
    try:
        subprocess.run(["nssm", "version"], check=True, capture_output=True)
    except FileNotFoundError:
        print("NSSM not found. Please install NSSM first:")
        print("1. Download NSSM from https://nssm.cc/")
        print("2. Extract and add to PATH")
        sys.exit(1)

    try:
        # Remove existing service if it exists
        subprocess.run(["nssm", "stop", "GoLinks"], check=False)
        subprocess.run(["nssm", "remove", "GoLinks", "confirm"], check=False)

        # Install new service
        run_command(["nssm", "install", "GoLinks", venv_python, app_path])
        run_command(["nssm", "set", "GoLinks", "AppDirectory", install_dir])
        run_command(["nssm", "set", "GoLinks", "DisplayName", "GoLinks Local Service"])
        run_command(["nssm", "set", "GoLinks", "Description", "Local URL shortener service"])
        run_command(["nssm", "set", "GoLinks", "Start", "SERVICE_AUTO_START"])
        run_command(["nssm", "start", "GoLinks"])
        print("Service installed and started successfully")
    except Exception as e:
        print(f"Error setting up service: {e}")
        sys.exit(1)

def main():
    if not is_admin():
        print("This script requires administrator privileges.")
        print("Please run as administrator")
        sys.exit(1)

    # Check for requirements.txt
    if not os.path.exists("requirements.txt"):
        print("requirements.txt not found in the current directory")
        sys.exit(1)

    setup_venv()
    setup_dns()
    setup_nssm()
    print("\nInstallation complete! Access golinks at http://go/go")
    print("Note: You may need to flush DNS cache: 'ipconfig /flushdns'")

if __name__ == "__main__":
    main()
