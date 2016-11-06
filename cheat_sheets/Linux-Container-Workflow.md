# Linux Container (LXC) Workflow

## Container Basics

These commands need root permissions, so either put a `sudo` in front of them or just become root with `sudo -i`.

### List containers
    lxc-ls --fancy

### Create a fresh Linux container
    lxc-create -t ubuntu -n mycontainername

### Start a container (daemonized, i.e. *not* attached to your current shell)
    lxc-start -n mycontainername -d

### Attach to a running container
    lxc-attach -n mycontainername

### Disconnecting from a container to which you've attached
Just run `logout`, `exit`, or type in Ctrl-d to detach from the container.

### Delete a container
    lxc-destroy -n mycontainername


## Prepping a (running) default `ubuntu` container for the first ansible run
To manually prep a container for the first ansible run, you'll need to install python and add your SSH key so that you can log in without a password.

* Check your container's IP address with `lxc-ls --fancy`
* Attach to your container with `lxc-attach -n mycontainername`
* Install Python 2 with `apt-get install python`
* In another shell, grab the SSH pubkey from the keypair you want to connect with (e.g. `cat ~/.ssh/id_rsa.pub`)
* In your container, create the SSH directory for the `ubuntu` user and add your key to allow login:
    mkdir /root/.ssh
    chmod 0700 /root/.ssh
    vi /root/.ssh/authorized_keys
    # in the vi editor, hit 'i' to enter insertmode , and then Ctrl(hold)-Shift(hold)-v(release) to paste your previously copied SSH pubkey
    
    # to save the file in vi, hit the 'esc' key and type ':wq' (no quotes) before hitting ENTER.
    # to quit without saving, hit the 'esc' key and type ':q!'
    # don't be scared, vi doesn't bite and it's no big deal if you screw something up at this point.
* Disconnect from the container with `Ctrl-d`
* Connect via SSH to the container for the first time, e.g. `ssh root@CONTAINER_IP`



## Running an Ansible playbook on a running container

* make sure the container's current IP is in your /etc/ansible/hosts file (or a local hosts file that you pass to ansible using the `-i` command-line option).
* `ansible-playbook playbookname.yml -u login_user`

For example, to run an nginx setup playbook stored in a file called nginx.yml, I'd run:
`ansible-playbook nginx.yml -u root`

There are many other options/arguments which you can add to this ansible-playbook command as well. Check the official Ansible documentation for details.


