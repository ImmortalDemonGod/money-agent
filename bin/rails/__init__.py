"""Verifier-side payment-rail registry (issue #30 Part 1).

Every scoreable source registers the same executable contract. A contribution may affect receive,
spend, or both, but it always carries its primary-source raw artifacts and fail-closed errors beside
the amount. `pnl.py` sums only successful, validated contributions; adapter exceptions become
verification errors rather than honest zeroes.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, FrozenSet


@dataclass
class RailContribution:
    name: str
    directions: FrozenSet[str]
    customer_usd: float = 0.0
    self_usd: float = 0.0
    unbound_usd: float = 0.0
    gross_usd: float = 0.0
    refunded_usd: float = 0.0
    fees_usd: float = 0.0
    spent_usd: float | None = 0.0
    spend_measured: bool = True
    raw_files: list[Path] = field(default_factory=list)
    raw_payloads: list[tuple[str, object]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    details: dict = field(default_factory=dict)

    def validate(self) -> None:
        if not self.directions or not self.directions <= {"receive", "spend"}:
            raise ValueError(f"{self.name}: directions must be receive and/or spend")
        for field_name in ("customer_usd", "self_usd", "unbound_usd", "gross_usd",
                           "refunded_usd", "fees_usd"):
            value = getattr(self, field_name)
            if not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
                raise ValueError(f"{self.name}: {field_name} must be finite and non-negative")
        if "spend" in self.directions:
            if self.spend_measured:
                if (not isinstance(self.spent_usd, (int, float))
                        or not math.isfinite(self.spent_usd) or self.spent_usd < 0):
                    raise ValueError(f"{self.name}: measured spent_usd must be finite and non-negative")
            elif self.spent_usd is not None:
                raise ValueError(f"{self.name}: unmeasured spend must be null, never zero")


@dataclass(frozen=True)
class RailAdapter:
    name: str
    directions: FrozenSet[str]
    pull: Callable[[], RailContribution]


class RailRegistry:
    def __init__(self) -> None:
        self._adapters: dict[str, RailAdapter] = {}

    def register(self, adapter: RailAdapter) -> None:
        if adapter.name in self._adapters:
            raise ValueError(f"duplicate rail adapter {adapter.name!r}")
        if not adapter.directions or not adapter.directions <= {"receive", "spend"}:
            raise ValueError(f"{adapter.name}: invalid adapter directions")
        self._adapters[adapter.name] = adapter

    def names(self) -> tuple[str, ...]:
        return tuple(self._adapters)

    def pull_all(self) -> list[RailContribution]:
        contributions: list[RailContribution] = []
        for adapter in self._adapters.values():
            try:
                result = adapter.pull()
                if result.name != adapter.name or result.directions != adapter.directions:
                    raise ValueError("contribution identity/directions do not match registration")
                result.validate()
            except Exception as exc:
                result = RailContribution(
                    name=adapter.name, directions=adapter.directions,
                    spent_usd=None if "spend" in adapter.directions else 0.0,
                    spend_measured=False if "spend" in adapter.directions else True,
                    errors=[f"{adapter.name}_adapter_failed: {type(exc).__name__}: {exc}"],
                )
            contributions.append(result)
        return contributions
