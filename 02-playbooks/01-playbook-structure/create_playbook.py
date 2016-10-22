#!/usr/bin/env python

HELP_TEXT = """
Usage: ./create_playbook.py /path/to/playbookname [role1 role2 ...]
Creates an empty playbook skeleton, with any roles that are specified.

e.g. ./create_plafybook.py /tmp/pyplaybook web db cache


If /path/to/playbookname already exists, we only create the roles that don't exist yet, according to our structure.


Our structure is loosely based on https://github.com/enginyoyen/ansible-best-practises:

###############################################################################
production.ini            # inventory file for production stage
development.ini           # inventory file for development stage
test.ini                  # inventory file for test stage
vpass                     # ansible-vault password file
                          # This file should not be committed into the repository
                          # therefore file is in ignored by git
group_vars/
    all/                  # variables under this directory belongs all the groups
        apt.yml           # ansible-apt role variable file for all groups
    webservers/           # here we assign variables to webservers groups
        apt.yml           # Each file will correspond to a role i.e. apt.yml
        nginx.yml         # ""
    postgresql/           # here we assign variables to postgresql groups
        postgresql.yml    # Each file will correspond to a role i.e. postgresql
        postgresql-password.yml   # Encrypted password file
roles/
    roles_requirements.yml# All the information about the roles
    external              # All the roles that are in git or ansible galaxy
                          # Roles that are in roles_requirements.yml file will be downloaded into this directory
    internal              # All the roles that are not public

extension/
    setup                 # All the setup files for updating roles and ansible dependencies
###############################################################################


I'm putting more emphasis on structured roles here, and less on external dependencies/playbooks.

"""

import sys
import os


def main():
    # Argument parsing
    args = sys.argv
    if len(args) < 2:
        print("Invalid invocation. Exiting.")
        print(HELP_TEXT)
        sys.exit(1)

    playbook_location = args[1]
    roles_to_create = args[2:]

    if playbook_location in ["help", "-h", "--help"]:
        print(HELP_TEXT)
        sys.exit(0)
    else:
        # this is a real path, let's make sure it's absolute
        playbook_location = os.path.abspath(playbook_location)

    # If that location already exists, fail
    if os.path.isdir(playbook_location) or os.path.isfile(playbook_location):
        print("Can't create a playbook with that path: something already exists there!")
        sys.exit(1)

    # Looks like everything is OK, let's create the playbook.
    print("Creating playbook skeleton")
    create_playbook(playbook_location)

    for r in roles_to_create:
        print("Creating role: ", r)
        create_role(playbook_location, r)


def create_playbook(location):
    """
    Create an empty playbook skeleton.
    """
    dirs_to_create = [
        "group_vars",
        "roles",
    ]
    files_to_create = [
        "production.ini",
        "development.ini",
        "hosts.ini",
        os.path.join("group_vars", "all")
    ]

    # Create the playbook skeleton
    print("Creating playbook directories")
    os.mkdir(location)
    for d in dirs_to_create:
        os.mkdir(os.path.join(location, d))

    print("Creating playbook files")
    for f in files_to_create:
        open(os.path.join(location, f), 'a').close()


def create_role(location, rolename):
    """
    Add a role to the playbook at LOCATION (an absolute path)
    """
    dirs_to_create = [
        os.path.join(location, "roles", rolename),
        os.path.join(location, "roles", rolename, "tasks"),
        os.path.join(location, "roles", rolename, "handlers"),
        os.path.join(location, "roles", rolename, "templates"),
        os.path.join(location, "roles", rolename, "files"),
        os.path.join(location, "roles", rolename, "vars"),
        os.path.join(location, "roles", rolename, "meta"),
    ]
    files_to_create = [
        os.path.join(location, "roles", rolename, "tasks", "main.yml"),
        os.path.join(location, "roles", rolename, "handlers", "main.yml"),
    ]

    # Create the role skeleton
    print("Creating role directories")
    for d in dirs_to_create:
        os.mkdir(os.path.join(location, d))

    print("Creating role files")
    for f in files_to_create:
        open(os.path.join(location, f), 'a').close()


# MAIN:
main()
