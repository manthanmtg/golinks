#!/usr/bin/env python3
import os
import subprocess
import sys
import ctypes

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

def stop_service():
    print("Stopping GoLinks service...")
    
    # Check if NSSM is available
    try:
        subprocess.run(["nssm", "version"], check=True, capture_output=True)
    except FileNotFoundError:
        print("NSSM not found. Please install NSSM first:")
        print("1. Download NSSM from https://nssm.cc/")
        print("2. Extract and add to PATH")
        sys.exit(1)

    try:
        # Stop and remove the service
        run_command(["nssm", "stop", "GoLinks"])
        run_command(["nssm", "remove", "GoLinks", "confirm"])
        print("Service stopped and removed successfully")
    except Exception as e:
        print(f"Error stopping service: {e}")
        sys.exit(1)

def main():
    if not is_admin():
        print("This script requires administrator privileges.")
        print("Please run as administrator")
        sys.exit(1)

    stop_service()
    print("\nGoLinks service has been stopped. You can restart it using golinks.py --start")

if __name__ == "__main__":
    main()
