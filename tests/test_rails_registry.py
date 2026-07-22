"""Executable contract tests for verifier-side payment rail registration."""

import math
import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))

from rails import RailAdapter, RailContribution, RailRegistry  # noqa: E402


class RailRegistryTests(unittest.TestCase):
    def test_aggregates_receive_and_spend_contributions(self) -> None:
        registry = RailRegistry()
        registry.register(
            RailAdapter(
                "receive",
                frozenset({"receive"}),
                lambda: RailContribution(
                    name="receive",
                    directions=frozenset({"receive"}),
                    customer_usd=2.5,
                ),
            )
        )
        registry.register(
            RailAdapter(
                "spend",
                frozenset({"spend"}),
                lambda: RailContribution(
                    name="spend",
                    directions=frozenset({"spend"}),
                    spent_usd=1.25,
                ),
            )
        )

        contributions = registry.pull_all()

        self.assertEqual(registry.names(), ("receive", "spend"))
        self.assertEqual(sum(item.customer_usd for item in contributions), 2.5)
        self.assertEqual(sum(item.spent_usd or 0 for item in contributions), 1.25)

    def test_rejects_duplicate_adapter_names(self) -> None:
        registry = RailRegistry()
        adapter = RailAdapter(
            "receive",
            frozenset({"receive"}),
            lambda: RailContribution(
                name="receive", directions=frozenset({"receive"})
            ),
        )
        registry.register(adapter)

        with self.assertRaises(ValueError):
            registry.register(adapter)

    def test_non_finite_contribution_fails_closed(self) -> None:
        registry = RailRegistry()
        registry.register(
            RailAdapter(
                "invalid",
                frozenset({"receive"}),
                lambda: RailContribution(
                    name="invalid",
                    directions=frozenset({"receive"}),
                    customer_usd=math.nan,
                ),
            )
        )

        contribution = registry.pull_all()[0]

        self.assertTrue(contribution.errors)
        self.assertEqual(contribution.customer_usd, 0.0)


if __name__ == "__main__":
    unittest.main()
