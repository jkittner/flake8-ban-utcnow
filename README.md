[![ci](https://github.com/jkittner/flake8-ban-utcnow/workflows/ci/badge.svg)](https://github.com/jkittner/flake8-ban-utcnow/actions?query=workflow%3Aci)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/jkittner/flake8-ban-utcnow/master.svg)](https://results.pre-commit.ci/latest/github/jkittner/flake8-ban-utcnow/master)

# flake8-ban-utcnow

flake8 plugin which checks that `datetime.utcnow()` and `datetime.utcfromtimestamp()` are not used. It suggests using `datetime.now(timezone.utc)` and `datetime.fromtimestamp(ts, tz=timezone.utc)`instead respectively.

Also, `utcnow` and `utcfromtimestamp` are finally deprecated in Python 3.12:

- PR: https://github.com/python/cpython/pull/103858
- Issue: https://github.com/python/cpython/issues/103857

**note:** timezone must be imported from `datetime` first:

```python
from datetime import datetime
from datetime import timezone

datetime.now(timezone.utc)
```

```python
from datetime import datetime
from datetime import timezone

datetime.fromtimestamp(1684079261, tz=timezone.utc)
```

## installation

```bash
pip install flake8-ban-utcnow
```

## flake8 code

| Code   | Description                                                                                                                                                                                     |
| ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| UTC001 | don't use datetime.datetime.utcnow(), use datetime.datetime.now(datetime.timezone.utc) instead or datetime.now(datetime.UTC) on >= 3.11.                                                        |
| UTC002 | don't use datetime.datetime.utcfromtimestamp(), use datetime.datetime.fromtimestamp(..., tz=datetime.timezone.utc) instead or datetime.datetime.fromtimestamp(..., tz=datetime.UTC) on >= 3.11. |

## as a pre-commit hook

See [pre-commit](https://pre-commit.com) for instructions

Sample `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/pycqa/flake8
  rev: 6.0.0
  hooks:
    - id: flake8
      additional_dependencies: [flake8-ban-utcnow==0.2.0]
```

## rationale

One could expect that when explicitly calling `datetime.utcnow()` the `datetime`
object would be timezone aware, but it's not! A common pitfall is, deriving a
timestamp from the `datetime` object created using `datetime.utcnow()`.

### example

- the computer is in `CEST` and we want to derive a `datetime` in **UTC**
  formatted as a timestamp hence calling `utcnow().timestamp()`.

  ```pycon
  >>> from datetime import datetime
  >>> datetime.utcnow()
  datetime.datetime(2022, 8, 7, 23, 40, 17, 7858)
  >>> datetime.utcnow().timestamp()
  1659908656.048843
  ```

- if we [convert](https://www.epochconverter.com/) the timestamp, it says this,
  which is obviously incorrect.

  ```
  GMT: Sunday, 7. August 2022 21:44:16
  Your time zone: Sunday, 7. August 2022 23:44:16 GMT+02:00 DST
  Relative: 2 hours ago
  ```

- converting it using python and `datetime.fromtimestamp`, we by accident get
  the correct datetime in **UTC**

  ```pycon
  >>> datetime.fromtimestamp(1659908656.048843)
  datetime.datetime(2022, 8, 7, 23, 44, 16, 48843)
  ```

- being aware that the timestamp _should_ be in `UTC` we call `utcfromtimestamp`
  instead and get the result as above, since the timestamp actually is in local
  time, but unaware of this.

  ```pycon
  >>> datetime.utcfromtimestamp(1659908656.048843)
  datetime.datetime(2022, 8, 7, 21, 44, 16, 48843)
  ```

### the correct way

- the computer is in `CEST` and we want to actually derive a `datetime` in **UTC**
  formatted as a timestamp.

  ```pycon
  >>> from datetime import timezone
  >>> from datetime import datetime
  >>> datetime.now(timezone.utc).timestamp()
  1659916399.651218
  ```

- we now get what we actually expect

  ```
  GMT: Sunday, 7. August 2022 23:53:19
  Your time zone: Monday, 8. August 2022 01:53:19 GMT+02:00 DST
  Relative: A few seconds ago
  ```

- the next thing to keep in mind is, that only timezone-aware `datetime` objects
  can be compared hence using this forces us to always make sure all objects are
  timezone aware.
