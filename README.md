# Key_Storage_System
Currently we use passwords to access personal accounts on different websites, which is why we usually forget them, so I have created this personal key storage system.

## Requirements

* [Click](https://click.palletsprojects.com/en/7.x/)
* [Tabulate](https://bitbucket.org/astanin/python-tabulate/src/master/)
* [Python-dotenv](https://github.com/theskumar/python-dotenv)

## Testing Application

The first thing is to verify if we have installed the [virtualenv](https://github.com/pypa/virtualenv) package in our operating system, in case of not having it installed, we run the following command to install it:
``` 
$ sudo pip install virtualenv
```
In the folder where we unzip it, we execute the command to start a new virtual environment:
```
$ virtualenv venv
```
To activate the virtual environment we activate the script:
```
$ source /path/to/venv/bin/activate
```
To undo these changes to your path (and prompt), just run:
```
$ deactivate
```
To test the application, install your package
```
$ /PATH/ pip install --editable .
```
## Usage

We execute the *__kss__* command, and it will immediately show us the help.