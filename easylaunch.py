#!/bin/python
import argparse
import os.path as path
from re import I
import tomli
import subprocess
import logging

DEFAULT_CONFIG_CONTENT = """
# Default config file for easylaunch

[example]
aliases = ["ex"] # [] by default
description = "Example Workspace" # "" by default
working-directory = "$HOME" # $HOME by default
commands = [
    "echo 'Hello World!'",
    "echo launching an app",
    "echo launching another app"
]

"""


parser = argparse.ArgumentParser(description='Easy Launch')

extra_commands = parser.add_mutually_exclusive_group(required=False)
# todo: add title and description to commands so they appear in separate groups


extra_commands.add_argument(
    "--version", help="print the version",
    action="store_const", const="version", dest="command"
)
extra_commands.add_argument(
    "--list", "-l", help="list all workspaces",
    action="store_const", const="list", dest="command"
)
extra_commands.add_argument(
    "--edit-config", help="edit the config file in you default editor", 
    action="store_const", const="edit-config", dest="command"
)
extra_commands.add_argument(
    "--load-default-config", help="load the default config file",
    action="store_const", const="load-default-config", dest="command"
)
extra_commands.add_argument(
    "--launch", help="launch a workspace",
    action="store_const", const="launch", dest="command"
)


parser.add_argument("--config", help="Specify the config file", required=False, default=path.expanduser("~/.config/easylaunch/config.toml"), dest="config")
parser.add_argument("--verbose", "-v", help="Enable verbose logging", required=False, default=False, dest="verbose", action="store_true")
parser.add_argument("workspaces", help="The workspace to launch", nargs="*")

parser.set_defaults(command="launch")

def run_command(command, *args, **kwargs):
    if isinstance(command, str):
        logging.debug(f"Running command: {command}")
    else :
        logging.debug(f"Running command: {' '.join(command)}")
    subprocess.run(command, *args, **kwargs)

def popen(command, *args, **kwargs):
    if isinstance(command, str):
        logging.debug(f"Popen command: {command}")
    else:
        logging.debug(f"Popen command: {' '.join(command)}")
    subprocess.Popen(command, *args, **kwargs)

def path_expand_all(path_str):
    return path.expanduser(path.expandvars(path_str))

def find_workspace(name, key, value):
    if key.lower() == name.lower():
        return True
    if "aliases" in value:
        for alias in value["aliases"]:
            if alias.lower() == name.lower():
                return True
    return False


def load_config(file_path):
    try:
        with open(file_path, "rb") as config_file:
            return tomli.load(config_file)
    except tomli.TOMLDecodeError as e:
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.error("Error while parsing config file.")
        else:
            logging.error("Error while parsing config file. Use verbode flag for more info")
        logging.debug(e)
        exit(1)

if __name__ == "__main__":
    
    # args, remaining_args = parser.parse_known_args()
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format="[ %(levelname)s ] %(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="[ %(levelname)s ] %(message)s")
    
    if not path.isfile(args.config) and args.command != "load_default_config":
        logging.error(f"Config file {args.config} does not exist")
        
    if args.command == "version":
        print("easylaunch 0.1.0")
        
    elif args.command == "edit-config":
        run_command(f"$EDITOR {args.config}", shell=True)
    
    elif args.command == "load-default-config":
        logging.info(f"Loading default config file at {args.config}")
        with open(args.config, "w") as f:
            f.write(DEFAULT_CONFIG_CONTENT) 
    
    elif args.command == "launch":
        
        # args = workspace_parser.parse_args(remaining_args, namespace=args) 

        if not args.workspaces:
            parser.parse_args(["--help"])

        config = load_config(args.config)
         
        for arg in args.workspaces: 

            found = False
            for workspace, values in config.items():
                if not isinstance(values, dict):
                    continue
                if find_workspace(arg, workspace, values):
                    workspace = values
                    found = True

            if found == False:
                logging.error(f"Workspace {arg} not found")
                continue
            

            if "working-directory" in workspace:
                working_directory = path_expand_all(workspace["working-directory"])
            else:
                working_directory = path_expand_all("$HOME") 
            
            # print(working_directory)
            if "commands" not in workspace:
                logging.warning(f"No commands found for workspace {arg}")
                continue
            
            logging.info("Launching workspace " + arg)
                
            for command in workspace["commands"]:
                popen(command, cwd=working_directory, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    elif args.command == "list":
        
        config = load_config(args.config)

        for workspace, values in config.items():
            if not isinstance(values, dict):
                continue
            print(workspace, end=" ")
            if "aliases" in values:
                print(" ".join(values["aliases"]), end=" ")
                print()
            if "description" in values and values["description"]:
                print(f"    {values['description']}")
            print()

