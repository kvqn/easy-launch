#!/bin/python
import argparse
import os.path as path
import tomli
import subprocess


parser = argparse.ArgumentParser(description='Easy Launch')
parser.add_argument("name", help="Name of the workspace")
parser.add_argument("--workdir", help="specify the working directory", required=False, default=path.expanduser("~/.config/easylaunch"))

if __name__ == "__main__":
    args = parser.parse_args()
    
    if not path.isdir(args.workdir):
        print("Workspace directory does not exist")
        exit(1)
        
    CONFIG_PATH = path.join(args.workdir, "config.toml")
    DEFAULT_CONFIG_PATH = path.join(args.workdir, "config.toml.default")
    
    try:
        with open(CONFIG_PATH, 'rb') as f:
            config = tomli.load(f)
    except FileNotFoundError:
        if not path.isfile(DEFAULT_CONFIG_PATH):
            raise FileNotFoundError("Default config file not found")
        
        subprocess.run(["cp", DEFAULT_CONFIG_PATH, CONFIG_PATH])
        print("Default config file copied to ~/.config/easylaunch/config")
        print("Do easylaunch-config to configure it")
        exit(0)  
        
    if not "workspaces" in config:
        print("No workspaces defined in config")
        exit(1)
    
    workspaces = config["workspaces"]
    
    if not args.name in workspaces:
        print("Workspace not found")
        exit(1)
        
    workspace = workspaces[args.name]
    
    if not isinstance(workspace, (tuple, list)):
        print("Workspace is not a list")
        exit(1)
    
    bad_config = False
    for command in workspace:
        if not isinstance(command, str):
            print("Command is not a string")
            bad_config = True
            break
    
    if bad_config:
        exit(1)
    
    for command in workspace:
        subprocess.Popen(command, shell=True)
    
    print("Launched workspace")