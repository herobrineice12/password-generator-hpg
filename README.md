## Console Password Generator
### Introduction
This is console password generator, as the name suggest, with the objective of creating cryptographic level passwords..

### Requirements
* Python 3 interpreter
* Argon2
* Pyperclip

You can install the second and the third requirements using pip. Normally pip already comes with the interpreter, but if you don't have, please visit this [official site] (https://docs.python.org/3/installing/index.html).

A example of a pip module installation is:
```
pip install module_name
```
If you are using arch linux:
```
sudo pacman -S python-module_name
```
This also works in arch, btw. If you wanna go through the risk of break your entire system
```
pip install --break-system-packages module_name
```

Also, it pays to remember that generally python `module_names` are separated with dashes (-).
### Usage
You can compile the project using the `pyinstaller` module with the command `pyinstaller Main.spec`, the output will be generated on the /dist/ directory