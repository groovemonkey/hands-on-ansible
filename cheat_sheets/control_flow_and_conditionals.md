# Control Flow and Conditionals in Ansible



## when

The basic conditional. The task runs if the "when" clause evaluates to "True".

    - name: If we're running systemd, create systemd unit file
      template: src=mattermost.service dest=/etc/systemd/system/mattermost.service
      when: systemd_installed.stat.exists


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

When a task is likely to produce errors in STDOUT, you can ignore them with ignore_errors.


## Is something defined?

    - name: Check if a variable is defined
      debug: msg="Yes, myvariable is defined."
      when: myvariable is defined



