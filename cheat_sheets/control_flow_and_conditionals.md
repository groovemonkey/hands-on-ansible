# Control Flow and Conditionals in Ansible

Official documentation here: http://docs.ansible.com/ansible/playbooks_loops.html


## when

The basic conditional. The task runs if the "when" clause evaluates to "True".

    - name: If we're running systemd, create systemd unit file
      template: src=mattermost.service dest=/etc/systemd/system/mattermost.service
      when: systemd_installed.stat.exists


    - command: /bin/emergencyshutoff
      when: result|failed
      # when: result|{succeeded,skipped}


## register

Register stores the output and state of a task in a variable.

    - stat: path={{ mattermost_directory }}
      register: mattermost_install

    - shell: whoami
      register: user_name

Registered variables can be used with the familiar curly-brace syntax:

    {{ user_name.stdout }}
    {{ user_name.stderr }}
    {{ mattermost_install.stat.exists == False }}



## Iteration

When iterators are used together with a `when`, the `when` is evaluated for *each* item. Careful, this means you can accidentally skip list items if you're making decisions based on them.
On the other hand, it allows you to sort or select only matching items, which can be useful.


### with_items

Iterates over a list:

    - name: COMMON | Install basic packages
      package: name={{ item }} state=present
      with_items:
        - wget
        - vim
        - nano
        - curl

If you've got a variable that points to a list, you can use that:

    with_items: "{{ my_wonderful_list }}"


### with_dict

You've defined a dictionary (YAML hash) like this:

    ---
    foods:
      pizza:
        woah: 3
        yum: 10
      curry:
        woah: 7
        yum: 10
      durian:
        woah: 11
        yum: 1
  
You can iterate over it like so:

    - name: Ruminate About Foods
      debug: msg="{{ item.key }} has an awesomeness of {{ item.value.woah }} and a deliciousness of {{ item.value.yum }}."
      with_dict: "{{ foods }}"



### with_nested

Nested loops! I've stolen the following from the official docs, since it's a great example:

    - name: Give users access to multiple databases
      mysql_user: name={{ item[0] }} priv={{ item[1] }}.*:ALL append_privs=yes password=foo
      with_nested:
        - [ 'alice', 'bob', 'dave' ]
        - [ 'clientdb', 'employeedb', 'providerdb', 'testdb' ]


## changed_when

Control when your task reports a change. This can be useful for things like "raw" or "shell" that always report a change (since Ansible can't know when they produce side effects on the target system).

e.g.

    - command: "apt-get upgrade -y"
      register: apt_upgrade
      changed_when: "'0 upgraded, 0 newly installed' not in apt_upgrade.stdout"
      # or
      # changed_when: "'Processing' in apt_upgrade.stdout"


## failed_when

    - command: "ls /some/nonexistent/dir"
      register: mylisting
      failed_when: "'foo' not in mylisting.stderr"
      ignore_errors: yes


## ignore_errors

When a task is likely to produce errors in STDERR, you can ignore them with ignore_errors.


## Is something defined?

    - name: Check if a variable is defined
      debug: msg="Yes, myvariable is defined."
      when: myvariable is defined



