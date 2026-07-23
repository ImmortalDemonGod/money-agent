"""Executable contract tests for verifier-side payment rail registration."""

import math
import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))

from rails import RailAdapter, RailContribution, RailRegistry  # noqa: E402


class RailRegistryTests(unittest.TestCase):
    def _invalid_contribution(self, adapter: RailAdapter) -> RailContribution:
        registry = RailRegistry()
        registry.register(adapter)
        contribution = registry.pull_all()[0]
        self.assertTrue(contribution.errors)
        self.assertEqual(contribution.customer_usd, 0.0)
        return contribution

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
        self._invalid_contribution(
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

    def test_adapter_exception_fails_closed(self) -> None:
        def explode() -> RailContribution:
            raise RuntimeError("primary source unavailable")

        self._invalid_contribution(
            RailAdapter("invalid", frozenset({"receive"}), explode)
        )

    def test_contribution_identity_and_direction_mismatch_fail_closed(self) -> None:
        for contribution in (
            RailContribution(name="other", directions=frozenset({"receive"})),
            RailContribution(name="invalid", directions=frozenset({"spend"})),
        ):
            with self.subTest(contribution=contribution):
                self._invalid_contribution(
                    RailAdapter(
                        "invalid", frozenset({"receive"}), lambda c=contribution: c
                    )
                )

    def test_negative_and_boolean_money_fail_closed(self) -> None:
        for amount in (-0.01, True, False):
            with self.subTest(amount=amount):
                self._invalid_contribution(
                    RailAdapter(
                        "invalid",
                        frozenset({"receive"}),
                        lambda value=amount: RailContribution(
                            name="invalid",
                            directions=frozenset({"receive"}),
                            customer_usd=value,
                        ),
                    )
                )

    def test_validate_directly_rejects_boolean_money(self) -> None:
        for contribution in (
            RailContribution(
                name="invalid", directions=frozenset({"receive"}), customer_usd=True
            ),
            RailContribution(
                name="invalid", directions=frozenset({"spend"}), spent_usd=False
            ),
        ):
            with self.subTest(contribution=contribution), self.assertRaises(ValueError):
                contribution.validate()

    def test_boolean_measured_spend_and_non_null_unmeasured_spend_fail_closed(self) -> None:
        invalid_spends = (
            RailContribution(
                name="invalid", directions=frozenset({"spend"}), spent_usd=True
            ),
            RailContribution(
                name="invalid",
                directions=frozenset({"spend"}),
                spent_usd=0.0,
                spend_measured=False,
            ),
        )
        for contribution in invalid_spends:
            with self.subTest(contribution=contribution):
                result = self._invalid_contribution(
                    RailAdapter(
                        "invalid", frozenset({"spend"}), lambda c=contribution: c
                    )
                )
                self.assertIsNone(result.spent_usd)
                self.assertFalse(result.spend_measured)


if __name__ == "__main__":
    unittest.main()
