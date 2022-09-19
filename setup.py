#!/bin/python
import argparse
import logging
import subprocess
import os

path = os.path

logging.basicConfig(level=logging.DEBUG)


parser = argparse.ArgumentParser(description='easy-launch setup')
parser.add_argument("--workdir", help="specify the working directory", required=False, default=path.expanduser("~/.config/easylaunch"))
parser.add_argument("--installdir", help="specify the installation directory where scripts will be installed", required=False, default=path.expanduser("~/.local/bin/"))
parser.add_argument("--source", help="specify the source directory where the source code is.", required=False, default=path.dirname(path.realpath(__file__)))
parser.add_argument("--reinstall", help="if scripts and configs already exist, replace them.", required=False, default=False, action="store_true")
parser.add_argument("--skip-aliases", help="don't make aliases in the zshrc", required=False, default=False, action="store_true")
parser.add_argument("--skip-config", help="don't make config files", required=False, default=False, action="store_true")
parser.add_argument("--create-symlinks", help="create symlinks instead of copying files", required=False, default=False, action="store_true", dest="create_symlinks")

def run_command(command, *args, **kwargs):
    if isinstance(command, str):
        logging.debug("Running command: %s", command)
    else:
        logging.debug(f"Running command: {' '.join(command)}")
    p = subprocess.run(command, *args, **kwargs)
    if p.returncode != 0:
        logging.error("Command failed: %s", command)
        exit(1)


if __name__ == "__main__":
    
    args = parser.parse_args()
    
    if not path.isdir(args.workdir):
        logging.info(f"Creating workspace directory {args.workdir}")
        os.mkdir(args.workdir)
    
    if not path.isdir(args.installdir):
        logging.info(f"Creating installation directory {args.installdir}")
        os.mkdir(args.installdir) 
        
    if not path.isdir(args.source):
        logging.info(f"Creating source directory {args.source}")
        os.mkdir(args.source)
        
    # This is a really good way to do this.
    PATHS = {
        "source/easylaunch.py": path.join(args.source, "easylaunch.py"),
        "source/config.default.toml": path.join(args.source, "config.default.toml"),
        "workdir/config.toml": path.join(args.workdir, "config.toml"),
        "workdir/config.default.toml": path.join(args.workdir, "config.default.toml"),
        "installdir/easylaunch": path.join(args.installdir, "easylaunch"),
        "bashrc": path.expanduser("~/.bashrc"),
        "zshrc": path.expanduser("~/.zshrc")
    }
    
    install = True
    if path.isfile(PATHS["installdir/easylaunch"]):
        if args.reinstall:
            logging.info(f"removed {PATHS['installdir/easylaunch']}")
            run_command(["rm", PATHS["installdir/easylaunch"]])
        else:
            install = False
            print("easylaunch already installed")
    
    if install:
        logging.info(f"Installing easylaunch to {PATHS['installdir/easylaunch']}")

        if args.create_symlinks:
            run_command(["ln", "-s", PATHS["source/easylaunch.py"], PATHS["installdir/easylaunch"]])
        else:
            run_command(["cp", PATHS["source/easylaunch.py"], PATHS["installdir/easylaunch"]])

        run_command(["chmod", "+x", PATHS["installdir/easylaunch"]])

        if not args.skip_aliases:
            run_command(f"echo \"alias launch='easylaunch'\" >> {PATHS['zshrc']}", shell=True)
            # run_command(f"echo \"alias launch='easylaunch'\" >> {PATHS['bashrc']}", shell=True)
    
   
    if not args.skip_config:
        install = True
        if path.isfile(PATHS["workdir/config.toml"]):
            if args.reinstall:
                logging.info(f"removed {PATHS['workdir/config.toml']}")
                run_command(["rm", PATHS["workdir/config.toml"]])
            else:
                install = False
                print("config.toml already installed")
        
        if install:
            logging.info(f"Installing config.toml to {PATHS['workdir/config.toml']}")
            run_command(["cp", PATHS["source/config.default.toml"], PATHS["workdir/config.toml"]])
        
    install = True 
    if path.isfile(PATHS["workdir/config.default.toml"]):
        if args.reinstall:
            logging.info(f"removed {PATHS['workdir/config.default.toml']}")
            run_command(["rm", PATHS["workdir/config.default.toml"]])
        else:
            install = False
            print("config.default.toml already installed")
            
    if install:
        logging.info(f"Installing config.default.toml to {PATHS['workdir/config.default.toml']}")
        run_command(["cp", PATHS["source/config.default.toml"], PATHS["workdir/config.default.toml"]])
    