# Nvidia (Ubuntu LTS)

# [Nvidia](https://docs.nvidia.com/datacenter/tesla/tesla-installation-notes/index.html#install-types)
```
sudo apt-get install linux-headers-$(uname -r)
```
```
distribution=$(. /etc/os-release;echo $ID$VERSION_ID | sed -e 's/\.//g')
wget https://developer.download.nvidia.com/compute/cuda/repos/$distribution/x86_64/cuda-keyring_1.0-1_all.deb
sudo dpkg -i cuda-keyring_1.0-1_all.deb
```
```
sudo apt-get update
sudo apt-get -y install cuda-drivers
```
