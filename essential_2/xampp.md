
#  XAMPP Installation & Usage Guide for Linux

##  Step 1: Download XAMPP

Go to [https://www.apachefriends.org/index.html](https://www.apachefriends.org/index.html)  
Choose the Linux version and download the `.run` installer (e.g., `xampp-linux-x64-8.0.30-0-installer.run`)

Or use `wget`:
```bash
wget https://www.apachefriends.org/xampp-files/8.0.30/xampp-linux-x64-8.0.30-0-installer.run
```

---

##  Step 2: Make Installer Executable

```bash
chmod +x xampp-linux-x64-8.0.30-0-installer.run
```

---

##  Step 3: Install XAMPP

Run the installer:
```bash
sudo ./xampp-linux-x64-8.0.30-0-installer.run
```

Follow the installation wizard.

---

##  Step 4: Start XAMPP

```bash
sudo /opt/lampp/lampp start
```

---

##  Step 5: Restart XAMPP

```bash
sudo /opt/lampp/lampp restart
```

---

##  Step 6: Stop XAMPP

```bash
sudo /opt/lampp/lampp stop
```

---

##  Step 7: Access phpMyAdmin

Open in browser:
```
http://localhost/phpmyadmin
```

---

##  Step 8: Add Your Project

Place your project files in:
```
/opt/lampp/htdocs/
```

Example:
```bash
sudo cp -r ~/my_project /opt/lampp/htdocs/
```

Access via browser:
```
http://localhost/my_project
```

---

##  Optional Fixes

**Install `net-tools` if netstat not found:**
```bash
sudo apt install net-tools
```

---
