# Troubleshooting and Debugging in Ansible

## Debug

    - name: Debugging!
      debug: msg="A debug message"

OR use var (they're mututally exclusive)

    - name: Debugging a variable!
      debug: var=somevar


## Register
Debug is often used in conjunction with 'register' to help you figure out what's going on.

    - shell: /usr/bin/uptime
      register: myuptime

    - name: Uptime Debugging
      debug: var=myuptime


You can add a 'verbosity' argument, which ensures that the debug output only runs when you pass -v, -vv, or -vvv options to Ansible on the command line.

    - name: Uptime, verbosity 1
      debug: var=myuptime verbosity=1

    - name: Uptime, verbosity 2
      debug: var=myuptime verbosity=2

    - name: Uptime, verbosity 3
      debug: var=myuptime verbosity=3



## Common Playbook Problems

Many of your errors will come from incorrect YAML syntax. The most common errors to check for are:

1. Not quoting an argument that starts with a variable, e.g.

    vars:
      age_path: {{ dave.age }}/html/oldman.html

If you start a value with a variable, you'll need to quote the whole thing:

    vars:
      age_path: "{{ dave.age }}/html/oldman.html"

See the YAML cheatsheet for more information.


2. Incorrect Indentation

You'll often have a task, block, or conditional that's indented one tab too many, or not indented enough. Ansible's error messages are getting better at narrowing down the errors and giving you a specific location to check, but this can still be wonky.

Make sure you're using consistent indentation!



## More Information

Check mode: http://docs.ansible.com/ansible/playbooks_checkmode.html

