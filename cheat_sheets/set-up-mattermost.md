# Setting up your Mattermost machine(s)

## Create Containers
You'll need to create these one at a time.

	sudo lxc-create -n mattermost -t ubuntu
	sudo lxc-create -n matterweb -t ubuntu
	sudo lxc-create -n matterdb -t ubuntu


### Start the Containers

	sudo lxc-start -n mattermost -d
	sudo lxc-start -n matterweb -d
	sudo lxc-start -n matterdb -d
	sudo lxc-ls -f


## Prep machines

You may have to ssh to each host first, if the ansible 2.2 regression is not fixed yet. Just add each host to your known_hosts by typing 'yes' and you'll be ready to go. Ansible version that have this bug fixed will not have to do this step first, and can directly run the commands below.

	cd /home/dave/code/hands-on-ansible/02-playbooks/00-simple-playbook-examples
	vim inv
	ansible-playbook prepare_ansible_target.yml -k --ask-sudo-pass -i inv


## Install Mattermost

	cd /home/dave/code/hands-on-ansible/02-playbooks/02-install-mattermost/install_mattermost
	vim hosts
	ansible-playbook install-mattermost.yml -i hosts
