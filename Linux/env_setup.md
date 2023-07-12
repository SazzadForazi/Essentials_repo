## Step 1 — Update and Upgrade
```
sudo apt update
sudo apt -y upgrade
```
### Step 2 — Check Version of Python
```
python3 -V
```
### Step 3 — Install pip
```
sudo apt install -y python3-pip
```
- ### pip3 install package_name
> Step 4 — Install Additional Tools(optional)
```
sudo apt install build-essential libssl-dev libffi-dev python3-dev
```
### Step 5 — Install venv
```
sudo apt install -y python3-venv
```
### Step 6 — Create a Virtual Environment
```
python3 -m venv my_env
```
### Step 7 — Activate Virtual Environment
```
source my_env/bin/activate
```
### Step 8 — Deactivate Virtual Environment
```
deactivate
```
### Upgrade packages
```
pip3 install --upgrade pip wheel setuptools
```
### install package from requirements.txt
```
pip3 install -r requirements.txt
```
### Create requirements.txt file
```
pip3 freeze > requirements.txt 
```
