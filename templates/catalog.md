Пицца из нашего меню:

{% for entry in catalog -%}
*{{ entry.title }} #{{loop.index}}*
{{ entry.description }}
    {%- for choice in entry.choices %}
        {{ choice.choice_title }} - *{{ choice.choice_price | int }} руб.*
    {%- endfor %}

{% endfor %}
