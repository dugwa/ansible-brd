The objective of this repo is to utilize Ansible to automate the provisioning of a new Litecoin Full Node.

The Full Node will be hosted in Digital Ocean and replicated across two or three more instances also within Digital Ocean.

Replication will be stored in Digital Ocean spaces (similar to AWS S3 service).

# Pre-Requisties 

i) install Virtualbox version >=6.1

https://www.wikihow.com/Install-VirtualBox

ii) install Vagrant >=2.2.16

https://www.vagrantup.com/downloads

https://www.vagrantup.com/docs/installation

We are going to be using vagrant to orchestrate our Ansible development machine (where we execute our Ansible code).

The aim is to make sure that we are executing Ansible from a universal and consistent platform. 

iii) create an ssh-key pair and name the private key file ```.private_key``` and move this file inside the ```ansible-code``` directory (don't worry the gitignore file won't check this in)


# Building the Ansible Dev Machine

Vagrant relies on Vagrantfile to build infrastructures.

The Vagrantfile at the root of this repository points to a settings.yaml (also on the root of this directory). 
You can add any customizations to your Ansible dev machine, such as: memory, hostname and IP address.

There is also a shared directory configured in the Vagrantfile to allow developers to continue using their favorite editor on their local workstation while the files being modified are updated in real-time inside the Vagrant machine. 

Take a look at this snippet 

```bash
vb.vm.synced_folder "./ansible-code", "/ansible-litecoin"
``` 

This will ensure that the local directory ansible-code will mounted on the guest machine (vm) as ansible-litecoin

In order to startup the Ansible Dev Machine, run the following commands 

```bash
vagrant up && vagrant ssh ansible
``` 

# Starting up the Litecoin Server on Digital Ocean
As you are now inside the Ansible devlopment manchine, you can run the following commands.

Firstly, we need to upload our ssh public key to digital ocean and take note of the ssh_key_id as we will need for the next command.

```bash
# export all environment variables 

# export your Digital Ocean token
export DO_API_TOKEN=***

# export Digital Ocean SPACES creds
export SPACES_ACCESS_KEY=***
export SPACES_SECRET_KEY=***
```

```bash
cd /ansible-litecoin

ansible-playbook ssh_keys.yml
```


```bash
export ANSIBLE_HOST_KEY_CHECKING=False

export PRIVATE_KEY_FILE=/ansible-litecoin/.private_key

# export your ssh_key_id from the output of ssh_keys.yml playbook
export SSH_KEY_ID=123456 

ansible-playbook --extra-vars ssh_key_id=${SSH_KEY_ID} digital_ocean.yml
``` 

# Litecoin FullNode Verification
```bash
# ping the litecoin node to verify it is up and running 
ansible all --inventory digital_ocean.py -m ping --private-key=.private_key --user=root
```

```bash
ansible all --inventory digital_ocean.py --private-key=.private_key --user=root -a "litecoin-cli getinfo"
``` 

```bash
# retrieve chain information
ansible all -i digital_ocean.py --private-key=.private_key --user=root -a "litecoin-cli getblockchaininfo"
``` 

# Backup of Litecoin
In order to backup the full node, all you need to is to run this playbook below.


```bash
ansible-playbook --extra-vars ssh_key_id=${SSH_KEY_ID} --inventory digital_ocean.py backup_litecoin.yml
```

This playbook will backup the litecoin data directory and copy it over to Digital Ocean spaces.


# Restore Litecoin
In order to deploy additional litecoin nodes, it makes sense to save some time by deploying from an already existing backup.

If you do not restore from a backup, then you will have to re-download the full copy of the Litecoin chain which is roughly about 20GB.

Run the following ansible playbook commands to deploy three additional nodes and restore from the backup that we have uploaded into spaces.

```bash
ansible-playbook --extra-vars ssh_key_id=${SSH_KEY_ID} --inventory digital_ocean.py restore_litecoin.yml
```

# Litecoin Restore Verification
Run the following commands to verify the data restore has worked
```bash
# ping the litecoin node to verify it is up and running 
ansible all --inventory digital_ocean.py -m ping --private-key=.private_key --user=root --limit=litecoin-restore
```

```bash
ansible all --inventory digital_ocean.py --private-key=.private_key --user=root --limit=litecoin-restore -a "litecoin-cli getinfo"
``` 

```bash
# retrieve chain information
ansible all -i digital_ocean.py --private-key=.private_key --user=root  --limit=litecoin-restore -a "litecoin-cli getblockchaininfo"
``` 

# Notes
If you decide to run this ansible playbooks without using Vagrant, all you need to is to install ansible-2.9.x on your local workstation and change into the ansible-code directory.

```bash
ansible --version
ansible 2.9.27
  config file = /etc/ansible/ansible.cfg
  configured module search path = [u'/home/vagrant/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python2.7/dist-packages/ansible
  executable location = /usr/bin/ansible
  python version = 2.7.17 (default, Feb 27 2021, 15:10:58) [GCC 7.5.0]
  

cd ansible-code
```