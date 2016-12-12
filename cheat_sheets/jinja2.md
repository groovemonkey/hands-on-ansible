# Jinja2: Useful Features

http://jinja.pocoo.org/docs/dev/templates/

## Delimiters

{% ... %} for Statements
{{ ... }} for Expressions to print to the template output
{# ... #} for Comments not included in the template output
#  ... ## for Line Statements




## Conditionals

See the "Control Flow and Conditionals" cheatsheet.


## 'For' Loops (Iteration)

Jinja2 supports the regular Python `for...in` loop, as long as you don't mind an additional "endfor" keyword.

    {# A list of webservers #}
    {% for server in groups['webservers'] %}
        web{{ loop.index }}.tutorialinux.org
    {% endfor %}


    {# A navigation menu #}
    <ul id="navigation">
        {% for item in navigation %}
            <li><a href="{{ item.href }}">{{ item.caption }}</a></li>
        {% endfor %}
    </ul>


## Filters

Filters are predefined functions that you can use in your Jinja templates. See the Jinja2 Filters Documentation here: http://jinja.pocoo.org/docs/dev/templates/#builtin-filters

For example, presuming you have a list of webservers (["server1", "server2"]). This might have been defined in a YAML file:

    webservers:
        - server1
        - server2


If you wanted to display all of these server names in a comma-separated string in your template, you might do:

    {{ webservers|join(', ') }}

"server1, server2" will be rendered as the template output.


## Escaping

Sometimes you want to render something exactly the way it appears, without having the Jinja2 parser get in the way.

    {% raw %}
        <ul>
        {% for item in seq %}
            <li>{{ item }}</li>
        {% endfor %}
        </ul>
    {% endraw %}

Everything inside of the 'raw' would be rendered literally.
