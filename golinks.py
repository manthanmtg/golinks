#!/usr/bin/env python3

import argparse
import importlib.util
import os
import platform
import sys

def get_platform():
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    return system

def import_script(name):
    script_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "scripts",
        f"{get_platform()}_golinks_{name}.py"
    )
    
    if not os.path.exists(script_path):
        print(f"Error: Platform-specific script not found: {script_path}")
        sys.exit(1)
        
    spec = importlib.util.spec_from_file_location(name, script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    parser = argparse.ArgumentParser(description="GoLinks service manager")
    parser.add_argument("--start", action="store_true", help="Start the GoLinks service")
    parser.add_argument("--stop", action="store_true", help="Stop the GoLinks service")
    
    args = parser.parse_args()
    
    if not (args.start or args.stop):
        parser.print_help()
        sys.exit(1)
        
    if args.start and args.stop:
        print("Error: Cannot specify both --start and --stop")
        sys.exit(1)
    
    action = "start" if args.start else "stop"
    try:
        script = import_script(action)
        if hasattr(script, "main"):
            script.main()
        else:
            print(f"Error: {action} script does not have a main() function")
            sys.exit(1)
    except Exception as e:
        print(f"Error executing {action} script: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
