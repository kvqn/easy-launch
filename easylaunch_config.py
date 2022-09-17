#!/bin/python
import argparse
import subprocess
import os.path as path


parser = argparse.ArgumentParser(description='Easy Launch Config')
parser.add_argument("--workdir", help="specify the working directory", required=False, default=path.expanduser("~/.config/easylaunch"))

if __name__ == "__main__":
    
    args = parser.parse_args()
    
    if not path.isdir(args.workdir):
        print("Workspace directory does not exist")
        exit(1)
        
    CONFIG_PATH = path.join(args.workdir, "config.toml")
    DEFAULT_CONFIG_PATH = path.join(args.workdir, "config.toml.default")
    
    if not path.isfile(CONFIG_PATH):
        if not path.isfile(DEFAULT_CONFIG_PATH):
            raise FileNotFoundError("Default config file not found")
        p = subprocess.run(["cp", DEFAULT_CONFIG_PATH, CONFIG_PATH])
        if p.returncode != 0:
            print("Failed to copy default config file")
            exit(1)
        print("Default config file copied to ~/.config/easylaunch/config.toml")
    
    subprocess.run(f"$EDITOR {CONFIG_PATH}", shell=True)