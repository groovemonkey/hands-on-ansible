#!/usr/bin/env python

import sys
import os


HELP_TEXT = """
Usage: ./create_playbook.py /path/to/playbookname [role1 role2 ...]
Creates an empty playbook skeleton, with any roles that are specified.

e.g. ./create_playbook.py /tmp/pyplaybook web db cache


If /path/to/playbookname already exists, we only create the roles that don't 
exist yet, according to our structure.


###############################################################################
group_vars/
    all                   # The main file for defining variables for this playbook

roles/
    role1/                # Each role
        files/            # Role-specific files which will be copied to the remote machine
        handlers/         # Role-specific handlers
            main.yml      # handler file
        tasks/            # Role-specific tasks
            main.yml      # task file
        templates/        # Role-specific templates
        vars              # Role-specific variables, although I recommend using group_vars/all instead
        meta/             # Files that establish role dependencies

###############################################################################


I'm putting more emphasis on well-structured roles here, and less on external 
dependencies/playbooks.

"""


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
        os.path.join("group_vars", "all"),
        "playbook.yml",
    ]

    # Create the playbook skeleton
    print("Creating playbook directories")
    os.mkdir(location, 0o755)
    for d in dirs_to_create:
        os.mkdir(os.path.join(location, d), 0o755)

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
        os.mkdir(os.path.join(location, d), 0o755)

    print("Creating role files")
    for f in files_to_create:
        open(os.path.join(location, f), 'a').close()


if __name__ == '__main__':
    main()
