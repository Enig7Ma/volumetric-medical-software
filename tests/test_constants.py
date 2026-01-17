from __future__ import annotations

from app.constants import IMAGING_TAGS, OTHER_TAGS, TAGS


def test_tags_are_concatenation() -> None:
    assert TAGS == [*IMAGING_TAGS, *OTHER_TAGS]


def test_tags_are_unique() -> None:
    # Not a strict requirement of the app, but helps keep the UI clean.
    assert len(TAGS) == len(set(TAGS))
