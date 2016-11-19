# Facts

Facts: information about hosts in your inventory that’s gathered by Ansible when it connects to a host.

You can use these facts in your plays – they are represented as variables stored in a dictionary.


Run the setup module to see facts.

	ansible 10.0.3.41 -m setup -u root



## Disable Fact Gathering

In some cases you do *not* want Ansible to automatically gather facts when it connects to a target machine. For example, this is often true when you manage system facts outside of Ansible, or when you are preparing a host that doesn't have Python installed.

You can disable fact gathering by setting ‘gather_facts: False’ at the playbook level (e.g. prepare_ansible_target.yml).



## Access Facts

Gathered facts are added to the Host variable scope. You can access them through the 'hostvars' dictionary.

	{{ hostvars[host]['fact_name'] }}



## Fact-testing tasks
Try running the following tasks on a host:

	- name: All the things
	  debug: msg={{ hostvars[inventory_hostname] }}

	- name: However this machine is listed in the inventory
	  debug: msg={{ inventory_hostname }}

	- name: Just the hostname
	  debug: msg={{ ansible_hostname }}

	- name: Just the primary IPv4 address
	  debug: msg={{ hostvars[inventory_hostname]['ansible_default_ipv4']['address'] }}

