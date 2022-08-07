import ast

import pytest

from flake8_ban_utcnow import Plugin

MSG = "UTC001 don't use datetime.utcnow(), use datetime.now(timezone.utc) instead"  # noqa: E501


def results(s):
    return {'{}:{}: {}'.format(*r) for r in Plugin(ast.parse(s)).run()}


@pytest.mark.parametrize(
    's',
    (
        'foo.utcnow()',
        'datetime.now(timezone.utc)',
    ),
)
def test_noop(s):
    assert not results(s)


@pytest.mark.parametrize(
    's',
    (
        'datetime.datetime.utcnow()',
        'datetime.utcnow()',
        'utcnow()',
    ),
)
def test_usage_of_utcnow(s):
    msg, = results(s)
    assert msg == f'1:0: {MSG}'


def test_in_function_default():
    s = 'def f(foo=utcnow()): ...'
    msg, = results(s)
    assert msg == f'1:10: {MSG}'


def test_as_assignment():
    s = 'foo = utcnow()'
    msg, = results(s)
    assert msg == f'1:6: {MSG}'


@pytest.mark.parametrize(
    's',
    (
        'foo = datetime.utcnow',
        'foo = datetime.datetime.utcnow',
    ),
)
def test_usage_of_utc_as_attribute_of_datetime(s):
    msg, = results(s)
    assert msg == f'1:6: {MSG}'
