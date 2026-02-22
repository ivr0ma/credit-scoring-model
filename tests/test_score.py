"""Тесты для model.score."""

import pytest
from model.score import predict


def test_predict_empty():
    assert predict([]) == 0.0


def test_predict_single():
    assert predict([1.0]) == 1.0
    assert predict([0.0]) == 0.0


def test_predict_bounds():
    assert 0 <= predict([0.5, 0.5]) <= 1.0
