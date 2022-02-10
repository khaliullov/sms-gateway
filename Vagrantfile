# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANT_PUBLIC_KEY = "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA6NF8iallvQVp22WDkTkyrtvp9eWW6A8YVr+kz4TjGYe7gHzIw+niNltGEFHzD8+v1I2YJ6oXevct1YeS0o9HZyN1Q9qgCgzUFtdOKLv6IedplqoPkcmF0aYet2PkEDo3MlTBckFXPITAMzF8dJSIFo9D8HfdOV0IAdx4O7PtixWKn5y2hMNG0zQPyUecp4pzC6kivAIhyfHilFR61RGL+GPXQ2MWZWFYbAGjyiYJnAmCP3NOTd0jMZEnDkbUvxhMmBYSdETk1rRgm+R4LOzFUGaHqHDLKLX+FIPKcF96hrucXzcWyLbIbEgE98OHlnVYCzRdK8jlqm8tehUc9c9WhQ== vagrant insecure public key"
ENV['VAGRANT_DEFAULT_PROVIDER'] ||= 'docker'
ENV['VAGRANT_CWD'] = '/vagrant'
DOCKER_PORTS = [ '8000:8000' ]

Vagrant.configure('2') do |config|
  config.vm.provider "docker" do |d|
    d.image = 'python:3.10.2'
    d.ports = DOCKER_PORTS
    d.force_host_vm = false
    d.has_ssh = true
    d.username = "vagrant"
    d.create_args = []
    d.cmd = ['/bin/bash', '-c'].push(%{
      echo "deb http://deb.debian.org/debian bullseye-backports main contrib non-free" >> /etc/apt/sources.list
      apt-get update
      apt-get upgrade -y
      apt-get install -y openssh-server locales sudo
      echo 'PubkeyAuthentication yes' >> /etc/ssh/sshd_config
      useradd --create-home --shell /bin/bash --user-group vagrant
      echo vagrant:vagrant | chpasswd
      sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen
      locale-gen --purge en_US.UTF-8
      echo 'LC_ALL=en_US.UTF-8' >> /etc/environment
      dpkg-reconfigure --frontend=noninteractive locales
      echo 'LANG="en_US.UTF-8"' > /etc/default/locale
      update-locale LANG=en_US.UTF-8
      echo "vagrant ALL=(ALL:ALL) NOPASSWD: ALL" >> /etc/sudoers
      mkdir -p /home/vagrant/.ssh
      echo "#{VAGRANT_PUBLIC_KEY}" > /home/vagrant/.ssh/authorized_keys
      chown -R vagrant:vagrant /home/vagrant
      chmod 0700 /home/vagrant/.ssh
      mkdir -p /var/run/sshd
      /usr/sbin/sshd -D -p 22
    })
  end

  config.vm.synced_folder ".", "/vagrant"

  config.vm.provision "shell", inline: <<-SHELL
    apt-get install -y \
		python3 \
		python3-pip \
		gammu \
		gammu-smsd \
		libgammu-dev \
		libmariadb-dev \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

    pip3 install -r /vagrant/src/requirements.txt

    echo "cd /vagrant" >> /home/vagrant/.profile
  SHELL

  config.vm.boot_timeout = 900

  config.ssh.host = "127.0.0.1"
  config.ssh.forward_agent = true
  config.ssh.extra_args = ['-A']
end
