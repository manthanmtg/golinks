#!/usr/bin/env python3
import os
import sys
import subprocess

def run_command(cmd):
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(cmd)}: {e}")
        sys.exit(1)

def stop_service():
    print("Stopping GoLinks service...")
    plist_path = os.path.expanduser("~/Library/LaunchAgents/com.user.golinks.plist")
    
    try:
        if os.path.exists(plist_path):
            run_command(["launchctl", "unload", plist_path])
            os.remove(plist_path)
            print("Service stopped and removed successfully")
        else:
            print("Service is not installed")
    except Exception as e:
        print(f"Error stopping service: {e}")
        sys.exit(1)

def main():
    stop_service()
    print("\nGoLinks service has been stopped. You can restart it using macos_golinks_start.py")

if __name__ == "__main__":
    main()
