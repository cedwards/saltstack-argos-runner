#!jinja|yaml

diff_path:
  file.managed:
    - name: {{ salt['config.get']('fim:diff_path') }}
    - source: salt://fim/fim.diff
    - template: jinja
    - show_diff: False
