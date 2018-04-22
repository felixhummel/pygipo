{% autoescape off %}SELECT
{{ column_definition | safe }}
FROM {{ view_name }}
WHERE entity = '{{ entity }}';{% endautoescape %}
