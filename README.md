```
# Run as a package module
$ python -m arnmap.arnmap
usage: arnmap.py [-h] --arn [ARN ...]

# Run using wrapper program
$ python arnmap-exec.py
usage: arnmap-exec.py [-h] --arn [ARN ...]
```
## arnmap.py
```
Class module. Includes an entry point and main method allowing it to be run directly.
```
## arnmap_helper.py
```
Helper module where resource specific methods are defined.
```
## arnmap_exec.py
```
Wrapper program to test importing the class module.
```
## Python Installation and Virtual Environment Setup
```
sudo apt update
sudo apt install python3
sudo apt-get install python3-venv
cd ~/
mkdir arnmap
cd ~/arnmap
python3 -m venv arnmap
dir ~/arnmap
source ~/arnmap/bin/activate
pip install boto3
pip list
deactivate
```
<!--
**arnmap/arnmap** is a ✨ _special_ ✨ repository because its `README.md` (this file) appears on your GitHub profile.

Here are some ideas to get you started:

- 🔭 I’m currently working on ...
- 🌱 I’m currently learning ...
- 👯 I’m looking to collaborate on ...
- 🤔 I’m looking for help with ...
- 💬 Ask me about ...
- 📫 How to reach me: ...
- 😄 Pronouns: ...
- ⚡ Fun fact: ...
-->
