# Task Blocks in Ansible

Blocks can be used for batching tasks together for easier and cleaner control flow, error handling, and cleanup.

A block starts with a "block:" statement, and can have (optional) "rescue" and "always" elements.

    block:
      - name: First item
        command: "ls /somedir"
        
        rescue:
          - name: Only run when a task inside the block throws an error.
            debug: msg="Something went wrong."
        always:
          - name: Always run.
            debug: msg="Regardless of what happened above, we're done with this block!"


A common use is to run an application download/unzip/install in the main task list of the block, put debugging output into the "rescue" tasklist, and then do cleanup in the "always" tasklist.
