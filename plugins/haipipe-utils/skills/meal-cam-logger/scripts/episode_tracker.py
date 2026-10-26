"""Episode-level segmentation for meal-cam.

Groups consecutive bite events into "eating episodes" by time gap. The
heuristic does not identify physical food items, so a food switch within an
episode may not trigger another Claude vision call.

An episode is defined as a sequence of bites where each bite is within
`max_gap_sec` of the previous one. A longer gap starts a new episode.

v0.3 — simple time-gap heuristic.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field


@dataclass
class Episode:
    """One time-gap episode of bite detections; it may contain several foods."""
    id: int
    start: dt.datetime
    end: dt.datetime
    bites: int
    labels: list[str] | None = None
    label_status: str = "pending"
    label_error_type: str | None = None
    label_model: str | None = None
    label_rubric: str | None = None
    label_input_sha256: str | None = None
    label_judged_at: str | None = None


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
        caller may classify only the first-bite frame and store the resulting
        labels plus identification status. A time-gap episode may include
        more than one food.
        Otherwise the bite is folded into the current episode and only the
        counter is updated.
        """
        if (self._current is None
                or (now - self._current.end).total_seconds() > self.max_gap_sec):
            # New episode
            ep = Episode(id=self._next_id, start=now, end=now, bites=1,
                         labels=None, label_status="pending")
            self._next_id += 1
            self._current = ep
            self._all.append(ep)
            return True, ep

        # Continue current episode
        self._current.end = now
        self._current.bites += 1
        return False, self._current

    def remove_last(self) -> Episode | None:
        """Remove the most recently logged episode, if one exists.

        This supports an explicit user correction during a session. If the
        removed episode was current, the next bite starts a fresh episode.
        Episode IDs remain monotonic for an unambiguous log.
        """
        if not self._all:
            return None
        removed = self._all.pop()
        if self._current is removed:
            self._current = None
        return removed

    @property
    def episodes(self) -> list[Episode]:
        return list(self._all)

    @property
    def current(self) -> Episode | None:
        return self._current
