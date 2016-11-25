# Ansible Variables

Variables are used for control flow, DRY (Don't Repeat Yourself), keeping things simple and manageable

Check out the [Official Ansible Variables Documentation](http://docs.ansible.com/ansible/playbooks_variables.html).

## Referencing Variables

- Use {{ varname }} syntax.


## Getting Variables into your Playbooks

### Setting variables directly in a Playbook file

	hosts: all 
	vars:
	  web_home_path: /var/www/home/ 
	  some_other_var: foombizzle
	tasks:
		...


### Relying on ansible-playbook knowing to look for variables in group_vars/all

The ansible-playbook command will expect the kind of playbook structure we use in this course. If you simply put your variables in your group_vars/all file, Ansible will find them and use them in playbook files.


### Explicitly Including a variables file from a playbook

	hosts: all
	include_vars: relpath/to/varsfile.yml
	include_vars: /abspath/to/varsfile.yml

	tasks:
	  ...


### Inventory File

	[webservers]
	web1.mydomain.com server_name="webking.mydomain.com"
	web2.mydomain.com server_name="webqueen.mydomain.com"
	 
	[webservers:vars]
	web_home_path=/var/www/home/



### Registering the result of a Task as a Variable

Often, you'll want to set a variable as the result of some Ansible task.

	tasks:
      - name: start nginx
        service: name=nginx state=started
        register: nginx_started


...Or for checking whether a file or directory exists, and then using 'when' for control flow based on that registered variable:

	- stat: path={{ mattermost_directory }}
	  register: mattermost_install

	- name: Some other task
	  module: arg1=foo arg2=bar
	  when: mattermost_install.stat.exists == False


### Passing variables in during ansible-playbook invocation

Use the '--extra-vars' flag to pass in variables for a playbook run from the command line.

	ansible-playbook deploy_application.yml --extra-vars "version=1.01 website_url=www.tutorialinux.com"

You can pass space-separated strings (as above) or quoted JSON through the --extra-vars parameter.


### Local Facts (more advanced)

Ansible reads facts dumped into files in /etc/ansible/facts.d/*.fact

These .fact files can be in INI or JSON format; they can even be executables that return JSON to stdout.


## Dictionaries (a.k.a. Hashes, Hashmaps, etc.)

	hosts: all 
	  vars:
	    web_home_path: /var/www/home/ 
	    dave:
	      last_name: Cohen
	      age: 72


Dictionaries can be accessed using Python dict notation *or* dot notation:

	dave['last_name'] or dave.last_name



## Reserved (Magic) Variables

Ansible sets a few variables for you, so don't overwrite them with other values:

hostvars: access variables and facts from other hosts.

group_names: a list of the groups that the current host is in.

groups: all groups (and all hostnames) in the inventory.

inventory_hostname: The current hostname that ansible is executing tasks on.

Additionally, the 'environment' variable is reserved by Ansible.

This is a bit more advanced than the basic Ansible material we're covering in this course, but feel free to read up on these for more information on how to use them.



## Variable Scopes

Ansible has three variable scopes (namespaces). Quoth the official Ansible documentation:

	Global: this is set by config, environment variables and the command line
	Play: each play and contained structures, vars entries, include_vars, role defaults and vars.
	Host: variables directly associated to a host, like inventory, facts or registered task outputs


## Variable Precedence

This list goes from 'most general' to 'most specific,' so variables that are defined in a place that's lower on this list "win" (shadow) variables that are higher up on this list:

Take a deep breath before reading. Everything will be OK.

1. role defaults
1. inventory vars
1. inventory group_vars
1. inventory host_vars
1. playbook group_vars
1. playbook host_vars
1. host facts
1. play vars
1. play vars_prompt
1. play vars_files
1. registered vars
1. set_facts
1. role and include vars
1. block vars (only for tasks in block)
1. task vars (only for the task)
1. extra vars (always win precedence)


It's nice to have this kind of fine-grained control (and a guarantee that this is ordered in a deterministic way), but you *do not* need to memorize this. Using all of these simultaneously will result in a hellishly complex constellation of variable scopes to manage, so beware.

You'll generally only use a few of these -- playbook variables, role variables, registered variables, occasional inventory group variables.


