# YAML

Ansible Playbooks are expressed in YAML. YAML is "Yet Another Markup Language," a human-readable, marchine-parsable serialized format for representing data across programming languages.

TLDR; It's like JSON, but with comments, and with indentation instead of curly brackets.

Let's take a look:

    ---
    # Simple variables (name = "Dave Cohen")
    name: Dave Cohen
    video_ideas: hundreds
    free_time: 0

    # List (books = ["Cryptonomicon", "Snow Crash" ... ])
    books:
        - Cryptonomicon
        - Snow Crash
        - The Design and Implementation of the FreeBSD Operating System
        - The Practice of Cloud System Administration

    # Dictionary ( languages = {"python": "excellent", "ruby": "good",  ... })
    languages:
        python: excellent
        ruby: good
        clojure: bad
        assembly: wannabe

    # Multi-line string: with newlines
    hobbies: |
        4 GCSEs
        3 A-Levels
        BSc in the Internet of Things

    # Multi-line string: one long line
    favorite_quote: >
        I just love 
        to read 
        lots of books


## Quoting 

YAML doesn't know about Ansible's jinja2 "{{ variable }}" syntax. When a YAML parser sees a '{' character which *isn't* in the middle of a string, it thinks it's seeing the beginning of a dictionary literal.

As a result, this won't work:

    vars:
      age_path: {{ dave.age }}/html/oldman.html
      # var     dict        stringWTF.IS.THIS.IDONTEVEN


If you start a value with a variable, you'll need to quote the whole thing:

    vars:
      age_path: "{{ dave.age }}/html/oldman.html"


This, however, would be fine, since the variable is in the middle of the value:

    vars:
      age_path: /www/{{ dave.age }}/html/oldman.html

Having the variable at the end of a value is fine, too. It's *only* an issue when the variable *starts* a value or parameter.

