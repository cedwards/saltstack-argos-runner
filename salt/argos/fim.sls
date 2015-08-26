fim_checksum:
  salt.state:
    - tgt: '*'
    - sls:
      - fim.checksum

cp_push_new:
  salt.function:
    - name: cp.push
    - tgt: '*'
    - arg:
      - {{ salt['config.get']('fim:new_path') }}
    - require:
      - salt: fim_checksum

fim_diff:
  salt.state:
    - tgt: {{ salt['config.get']('master') }}
    - sls:
      - fim.diff
    - require:
      - salt: cp_push_new

fim.rotate:
  salt.function:
    - tgt: {{ salt['config.get']('master') }}
    - require:
      - salt: fim_diff

