### Installation using the docker repository

# Remvoe any old versions of docker
sudo apt-get remove docker docker-engine docker.io containerd runc

sudo apt-get update

# Install docker 
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

# Add Docker’s official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

#Verify that you now have the key with the fingerprint 9DC8 5822 9FC7 DD38 854A  E2D8 8D81 803C #0EBF CD88
sudo apt-key fingerprint 0EBFCD88


# set up the stable repository
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update

# List docker versions
# apt-cache madison docker-ce

# Install docker engine
sudo apt-get install docker-ce='5:19.03.11~3-0~ubuntu-xenial' docker-ce-cli='5:19.03.11~3-0~ubuntu-xenial' containerd.io

# Run docker without sudo
sudo groupadd docker
sudo gpasswd -a $USER docker
newgrp docker
docker login
