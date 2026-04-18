"""Tests for flappy_bird_demo.score."""

import pytest

from flappy_bird_demo.score import Score


@pytest.fixture
def score() -> Score:
    return Score()


def test_initial_score_zero(score: Score) -> None:
    assert score.current == 0
    assert score.high == 0


def test_increment_score(score: Score) -> None:
    score.increment()
    assert score.current == 1


def test_reset_preserves_high_score(score: Score) -> None:
    for _ in range(5):
        score.increment()
    score.reset()
    assert score.high == 5


def test_high_score_updates_on_reset(score: Score) -> None:
    for _ in range(5):
        score.increment()
    score.reset()
    for _ in range(3):
        score.increment()
    score.reset()
    assert score.high == 5


def test_reset_clears_current(score: Score) -> None:
    score.increment()
    score.increment()
    score.reset()
    assert score.current == 0
