import ast

import pytest

from flake8_ban_utcnow import Plugin

UTC001 = "UTC001 don't use datetime.datetime.utcnow(), use datetime.datetime.now(datetime.timezone.utc) instead or datetime.now(datetime.UTC) on >= 3.11."  # noqa: E501
UTC002 = "UTC002 don't use datetime.datetime.utcfromtimestamp(), use datetime.datetime.fromtimestamp(..., tz=datetime.timezone.utc) instead or datetime.datetime.fromtimestamp(..., tz=datetime.UTC) on >= 3.11."  # noqa: E501


def results(s):
    return {'{}:{}: {}'.format(*r) for r in Plugin(ast.parse(s)).run()}


@pytest.mark.parametrize(
    's',
    (
        'foo.utcnow()',
        'foo.utcfromtimestamp(ts)',
        'datetime.now(timezone.utc)',
        'datetime.fromtimestamp(ts, tz=timezone.utc)',
        'datetime.datetime.now(timezone.utc)',
        'datetime.datetime.fromtimestamp(ts, tz=timezone.utc)',
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
    assert msg == f'1:0: {UTC001}'


@pytest.mark.parametrize(
    's',
    (
        'datetime.datetime.utcfromtimestamp(ts)',
        'datetime.utcfromtimestamp(ts)',
        'utcfromtimestamp(ts)',
    ),
)
def test_usage_of_utcfromtimestamp(s):
    msg, = results(s)
    assert msg == f'1:0: {UTC002}'


def test_utcnow_in_function_default():
    s = 'def f(foo=utcnow()): ...'
    msg, = results(s)
    assert msg == f'1:10: {UTC001}'


def test_utcfromtimestamp_in_function_default():
    s = 'def f(foo=utcfromtimestamp(ts)): ...'
    msg, = results(s)
    assert msg == f'1:10: {UTC002}'


def test_utcnow_as_assignment():
    s = 'foo = utcnow()'
    msg, = results(s)
    assert msg == f'1:6: {UTC001}'


def test_utcfromtimestamp_as_assignment():
    s = 'foo = utcfromtimestamp(ts)'
    msg, = results(s)
    assert msg == f'1:6: {UTC002}'


@pytest.mark.parametrize(
    's',
    (
        'foo = datetime.utcnow',
        'foo = datetime.datetime.utcnow',
    ),
)
def test_usage_of_utcnow_as_attribute_of_datetime(s):
    msg, = results(s)
    assert msg == f'1:6: {UTC001}'


@pytest.mark.parametrize(
    's',
    (
        'foo = datetime.utcfromtimestamp',
        'foo = datetime.datetime.utcfromtimestamp',
    ),
)
def test_usage_of_utcfromtimestamp_as_attribute_of_datetime(s):
    msg, = results(s)
    assert msg == f'1:6: {UTC002}'
