#!jinja|yaml

fim_path:
  file.managed:
    - name: {{ salt['config.get']('fim:fim_path') }}
    - source: salt://fim/fim.new
    - template: jinja
    - show_diff: False
