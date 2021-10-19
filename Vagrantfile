# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'yaml'
settings = YAML.load_file 'settings.yml'

VAGRANTFILE_API_VERSION="2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  # General Vagrant VM configuration.
  config.ssh.insert_key = false
  config.vm.provider :virtualbox do |v|
    v.memory = settings['memory']
    v.linked_clone = true
  end

  # Ansible Machine
  config.vm.define "ansible" do |vb|
    vb.vm.synced_folder "./ansible-code", "/ansible-litecoin"
    vb.vm.hostname = settings['hostname']
    vb.vm.network :private_network, ip: settings['ip']
    vb.vm.box = "ubuntu/bionic64"
    vb.vm.provision "ansible" do |ansible|
      ansible.playbook = "playbook.yml"
    end
  end

end



