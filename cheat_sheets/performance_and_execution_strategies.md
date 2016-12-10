# Performance and Execution Strategies in Ansible 2.0

## Two Execution Strategies:

Execution strategies tell ansible how to go about executing plays on hosts. Should all hosts just let loose and try to 

1. linear (default):

- one task at a time, across all servers
    - can be problematic if some servers are slower than others, haven't cached package lists, etc.
- takes a 'serial' argument where you define chunk size

    - name: Do that thing with the thing, two servers at a time.
      hosts: webservers
      serial: 2

    - name: Do this thing on 30% of my servers at a time.
      hosts: webservers
      serial: "30%"


    - name: Define multiple batch sizes (in absolute target host numbers or %)
      hosts: webservers
      serial:
      - 1
      - 5
      - 10%


2. free: a race to the end of the play -- every target host for itself!

Provided you have enough forks, this will let hosts blast through their tasks as fast as they can.

    - hosts: all
      strategy: free
      tasks:
        ...



## Max Failure Percentage

If you're deploying out to a large fleet of servers, some things will fail (for whatever reason). If you're doing this, you've already *thoroughly* tested your playbook, so you may be confident that everything is fine.

However, it can be good to make sure you abort in case you have an unexpectedly high failure rate (indicating that you're not quite done with testing the playbook).

    - hosts: webservers
      max_fail_percentage: 5
      serial:
        - 10%

This way, you'll abort the whole thing if more than 5% of your target hosts fail.


## Performance

Most of your time waiting will be spent on package cache updates, package installs, artifact downloads (e.g. WordPress).

Here are some of the things you can do to get more performance out of Ansible:

- Use local package servers for your server fleet (speeds cache updates and package installs).
- Use with_items for installing packages (ansible knows to roll these into a single package manager transaction)
- Use ControlPersist with OpenSSH, setting a reasonable timeout. Beware of memory limits if you're dealing with thousands of servers.
- Pipelining (if you're not using 'sudo' on target hosts): http://docs.ansible.com/ansible/intro_configuration.html#pipelining

