#!/usr/bin/env python3
import os
import sys
import subprocess
import venv
from pathlib import Path

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
            venv_pip = os.path.join("venv", "bin", "pip")
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
    hosts_path = "/etc/hosts"
    
    # Check if entry already exists
    with open(hosts_path, 'r') as f:
        if hosts_line in f.read():
            print("DNS entry already exists")
            return

    try:
        run_command(["sudo", "sh", "-c", f'echo "{hosts_line}" >> {hosts_path}'])
        print("DNS entry added successfully")
    except Exception as e:
        print(f"Error setting up DNS: {e}")
        print("Please manually add '127.0.0.1 go' to /etc/hosts")

def create_launch_agent():
    print("Setting up launch agent...")
    install_dir = os.path.abspath(os.path.dirname(__file__))
    venv_python = os.path.join(install_dir, "venv", "bin", "python3")
    app_path = os.path.join(install_dir, "app.py")
    
    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.golinks</string>
    <key>ProgramArguments</key>
    <array>
        <string>{venv_python}</string>
        <string>{app_path}</string>
    </array>
    <key>WorkingDirectory</key>
    <string>{install_dir}</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>~/.golinks/golinks.log</string>
    <key>StandardErrorPath</key>
    <string>~/.golinks/golinks.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
</dict>
</plist>
"""

    # Create LaunchAgents directory if it doesn't exist
    launch_agents_dir = os.path.expanduser("~/Library/LaunchAgents")
    os.makedirs(launch_agents_dir, exist_ok=True)

    # Write and load the launch agent
    plist_path = os.path.join(launch_agents_dir, "com.user.golinks.plist")
    try:
        with open(plist_path, "w") as f:
            f.write(plist_content)
        run_command(["launchctl", "unload", plist_path])
        run_command(["launchctl", "load", plist_path])
        print("Launch agent installed and started successfully")
    except Exception as e:
        print(f"Error setting up launch agent: {e}")
        sys.exit(1)

def main():
    # Check for requirements.txt
    if not os.path.exists("requirements.txt"):
        print("requirements.txt not found in the current directory")
        sys.exit(1)

    setup_venv()
    setup_dns()
    create_launch_agent()
    print("\nInstallation complete! Access golinks at http://go/go")

if __name__ == "__main__":
    main()
