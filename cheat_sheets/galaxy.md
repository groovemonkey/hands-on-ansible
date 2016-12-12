# Ansible Galaxy


    ansible-galaxy install username.role_name
    ansible-galaxy install tutorialinux.nginx,v1.8.24
    ansible-galaxy install git+https://github.com/groovemonkey/nginx.git
    ansible-galaxy install -r requirements.yml (roles file)
    sudo ansible-galaxy remove some.role

Roles are installed in /etc/ansible/roles/ by default. You can configure this in /etc/ansible/ansible.cfg or with the --roles-path argument.

    ansible-galaxy install --roles-path . jeqo.nginx



## Practical

### Download a role

    sudo ansible-galaxy install jeqo.nginx
    ansible-galaxy list


### Create a playbook that uses this role

nano test.yml

    - hosts: all
      roles:
      - { role: jeqo.nginx }


ansible-playbook test.yml -i hosts -u ubuntu -k --ask-sudo-pass



