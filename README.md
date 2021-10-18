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
