
import datetime
import pytest

from src.algorithms import sm2


def test_invalid_quality():
    with pytest.raises(ValueError):
        sm2.update_sm2_stats(2.5, 0, 0, 6)


def test_reset_on_failure(monkeypatch):
    class FixedDatetime(datetime.datetime):
        @classmethod
        def utcnow(cls):
            return datetime.datetime(2024, 1, 1)

    monkeypatch.setattr(sm2, 'datetime', FixedDatetime)
    res = sm2.update_sm2_stats(2.5, 3, 10, 1)
    assert res['repetitions'] == 0
    assert res['interval'] == 1
    assert res['easiness_factor'] >= 1.3
    assert res['next_due'] == FixedDatetime.utcnow() + datetime.timedelta(days=1)


def test_successful_review(monkeypatch):
    class FixedDatetime(datetime.datetime):
        @classmethod
        def utcnow(cls):
            return datetime.datetime(2024, 1, 1)

    monkeypatch.setattr(sm2, 'datetime', FixedDatetime)
    res = sm2.update_sm2_stats(2.5, 1, 1, 5)
    assert res['repetitions'] == 2
    assert res['interval'] == 6
    assert res['easiness_factor'] > 2.5


def test_late_repetition(monkeypatch):
    class FixedDatetime(datetime.datetime):
        @classmethod
        def utcnow(cls):
            return datetime.datetime(2024, 1, 1)

    monkeypatch.setattr(sm2, 'datetime', FixedDatetime)
    res = sm2.update_sm2_stats(2.5, 5, 12, 5)
    assert res['repetitions'] == 6
    assert res['interval'] == round(12 * 2.5)
    assert res['easiness_factor'] > 2.5
    assert res['next_due'] == FixedDatetime.utcnow() + datetime.timedelta(days=res['interval'])
