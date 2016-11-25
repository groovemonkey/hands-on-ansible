# Jinja2: useful Features

## Conditionals

See the "Control Flow and Conditionals" cheatsheet.


## Loops

Jinja2 supports the regular Python `for...in` loop, as long as you don't mind an additional "endfor" keyword.

    # A list of webservers
    {% for server in groups['webservers'] %}
        web{{ loop.index }}.tutorialinux.org
    {% endfor %}


