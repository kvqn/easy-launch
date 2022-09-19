# easylaunch

A simple tool to launch multiple commands at once.

### Table of Contents

- [Usage](#usage)
  
  - [Launching a Workspace](#launch-a-workspace)
  - [Other Actions](#other-actions)
  - [Available Options](#available-options)

- [Configuration](#configuration)

- [Installation](#installation)
  
  - [Quick Installation](#quick-installtion)
  - [Setup Option](#setup-options)

# Usage

### Launch a workspace

This is the default action that easylaunch performs.

```
easylaunch <name of workspace>
```

### Other actions

```
--help, -h                show the help message and exit
--version                 show the version and exit
--list, -l                list all workspaces
--edit-config             open the config file in your default editor
--load-default-config     replace the config file with the default config file
--launch                  default action is to launch a workspace.
```

### Available options

```
--verbose, -v             verbose output
--config                  specify a config file
```

# Configuration

Refer to the [default config file](/config.default.toml) for the example configuration. It's a pretty obvious structure.

### Example Configuration

```TOML
[example]
aliases = ["ex"] # [] by default
description = "Example Workspace" # "" by default
working-directory = "$HOME" # $HOME by default
commands = [
    "echo 'Hello World!'",
    "echo launching an app",
    "echo launching another app"
]
```

The configuration format is TOML. Refer here [GitHub : TOML](https://github.com/toml-lang/toml).

Each section is a workspace. The section name and provided aliases will be used to refer to that workspace.

`aliases` - \[List : str\] set aliases for the workspace

`description` - \[str\] describe your worksapce

`working-directory` - \[str\] valid directory path where the shell commands will be executed.

`commands` - \[list : str\] list of commands to be executed.

**note** : the commands are executed in separate shells. so don't expect that `cd` will change the working directory for the commands below it. 

# Installation

### Quick Installtion

```
git clone --depth=1 https://github.com/kevqn11/easy-launch.git
cd easy-launch
python setup.py
```

### Setup Options

```
options:
  -h, --help            show this help message and exit
  --workdir workdir     specify the working directory
  --installdir installdir
                        specify the installation directory where scripts will be installed
  --source source       specify the source directory where the source code is.
  --reinstall           if scripts and configs already exist, replace them.
  --skip-aliases        don't make aliases in the zshrc
  --skip-config         don't make config files
  --create-symlinks     create symlinks instead of copying files
```


By default, the installation script will add the following statement in .zshrc of the user.

> alias launch='easylaunch'

to prevent this you can use the `--skip-aliases` option.



`--reinstall` can be used to update the app. but it will also replace the configuration files and create more (redundant) aliases in zshrc. use `--skip-config` and `--skip-aliases` to prevent that.