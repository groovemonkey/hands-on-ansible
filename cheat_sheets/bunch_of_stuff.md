# Various tips and tricks

## Waiting before starting a task

Sometimes you need to wait for something to happen. For example, when you wait for a third party (e.g. AWS) to finish provisioning something.

    - name: Wait for SSH to come up
      wait_for: host={{ item.public_dns_name }} port=22 delay=60 timeout=320 state=started
      with_items: '{{ ec2.instances }}'


Other examples:

    wait: yes
    wait_for: state=started host={{ myhost }} port=1234 delay=60 timeout=320
    wait_for: host="{{ myamazonhost['instance'].status == 'available' }}" port=1234 delay=60 timeout=320 state=started
    wait_timeout: 600



## Running ansible tasks on your local machine

Run from the command line with --connection=local. For example:

    ansible-playbook do_local_stuff.yml --connection=local


