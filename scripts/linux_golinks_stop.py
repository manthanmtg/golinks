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
    service_path = "/etc/systemd/system/golinks.service"
    
    try:
        if os.path.exists(service_path):
            run_command(["sudo", "systemctl", "stop", "golinks"])
            run_command(["sudo", "systemctl", "disable", "golinks"])
            run_command(["sudo", "rm", service_path])
            run_command(["sudo", "systemctl", "daemon-reload"])
            print("Service stopped and removed successfully")
        else:
            print("Service is not installed")
    except Exception as e:
        print(f"Error stopping service: {e}")
        sys.exit(1)

def main():
    if os.geteuid() != 0:
        print("This script requires sudo privileges to stop the service.")
        print("Please run: sudo python3 linux_golinks_stop.py")
        sys.exit(1)

    stop_service()
    print("\nGoLinks service has been stopped. You can restart it using golinks.py --start")

if __name__ == "__main__":
    main()
