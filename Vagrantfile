# -*- mode: ruby -*-
# vi: set ft=ruby :

# Ruby function to determine if we are running on an M1 Mac
def m1?
  `uname -m`.strip == "arm64"
end

if m1?
  BOX = "perk/ubuntu-2204-arm64"
else
  BOX = "generic/ubuntu2204"
end

Vagrant.configure("2") do |config|
  config.vm.box = BOX
  config.vm.synced_folder ".", "/vagrant"
  config.vm.provision "shell", path: "install.py"
end
