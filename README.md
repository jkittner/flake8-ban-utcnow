[![ci](https://github.com/theendlessriver13/flake8-ban-utcnow/workflows/ci/badge.svg)](https://github.com/theendlessriver13/flake8-ban-utcnow/actions?query=workflow%3Aci)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/theendlessriver13/flake8-ban-utcnow/master.svg)](https://results.pre-commit.ci/latest/github/theendlessriver13/flake8-ban-utcnow/master)

# flake8-ban-utcnow

flake8 plugin which checks that `dateimte.utcnow()` is not used. It suggests using `datetime.now(timezone.utc)` instead.

**note: ** `timezone must be imported from datetime first`:

```python
from datetime import datetime
from datetime import timezone

datetime.now(timezone.utc)
```

## installation

`pip install flake8-ban-utcnow`

## flake8 code

| Code   | Description                                                             |
| ------ | ----------------------------------------------------------------------- |
| UTC001 | don't use `datetime.utcnow()`, use `datetime.now(timezone.utc)` instead |

## as a pre-commit hook

See [pre-commit](https://pre-commit.com) for instructions

Sample `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/pycqa/flake8
  rev: 5.0.4
  hooks:
    - id: flake8
      additional_dependencies: [flake8-ban-utcnow==0.1.0]
```
