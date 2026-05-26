"""Episode-level segmentation for meal-cam.

Groups consecutive bite events into "eating episodes" so that one physical
food item triggers exactly ONE Claude vision call, regardless of how many
bites the user takes from it.

An episode is defined as a sequence of bites where each bite is within
`max_gap_sec` of the previous one. A longer gap starts a new episode.

v0.3 — simple time-gap heuristic. Future (v0.3.1): also check spatial
coherence of the hand's "source" position to catch food-switches that
happen without a long pause.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field


@dataclass
class Episode:
    """One contiguous eating episode — a single food item over N bites."""
    id: int
    start: dt.datetime
    end: dt.datetime
    bites: int
    label: str | None          # filled in after the Claude call on the first bite
    first_frame_b64: str | None = None  # retained in case of re-identification


@dataclass
class EpisodeTracker:
    """Stateful tracker: decides whether each bite starts a new episode."""

    max_gap_sec: float = 45.0
    _next_id: int = field(default=1, init=False)
    _current: Episode | None = field(default=None, init=False)
    _all: list[Episode] = field(default_factory=list, init=False)

    def on_bite(self, now: dt.datetime) -> tuple[bool, Episode]:
        """Call on every bite event from BiteDetector.

        Returns (is_new_episode, episode).  If is_new_episode is True, the
        caller should run the Claude vision call and set episode.label /
        episode.first_frame_b64.  Otherwise the bite is folded into the
        current episode and only the counter is updated.
        """
        if (self._current is None
                or (now - self._current.end).total_seconds() > self.max_gap_sec):
            # New episode
            ep = Episode(id=self._next_id, start=now, end=now, bites=1, label=None)
            self._next_id += 1
            self._current = ep
            self._all.append(ep)
            return True, ep

        # Continue current episode
        self._current.end = now
        self._current.bites += 1
        return False, self._current

    @property
    def episodes(self) -> list[Episode]:
        return list(self._all)

    @property
    def current(self) -> Episode | None:
        return self._current
