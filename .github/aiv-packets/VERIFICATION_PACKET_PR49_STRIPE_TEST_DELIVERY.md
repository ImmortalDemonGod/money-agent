# AIV Verification Packet — PR49 Stripe Test Delivery

Author: ImmortalDemonGod  
Verifier: Codex

## 0. Logical unit

External acceptance evidence for #39. A Stripe **test-mode** $1 product, Price, and Payment Link
were created with `restrictions.completed_sessions.limit=1` and a provider-configured completion
redirect to `https://one-honest-dollar.cloud-pyramid.workers.dev/`.

## 1. Classification

```yaml
classification:
  risk_tier: R3
  sod_mode: S0
  critical_surfaces: [payments, delivery]
  blast_radius: service
  classification_rationale: >
    This records a real payment-delivery acceptance check. It uses Stripe test mode only and
    changes no live payment surface.
```

## 2. Claim

CLM-001: The test Payment Link is provider-capped at one completed session and its configured
success redirect serves a complete public artifact. Falsified by a non-1 limit, redirect mismatch,
HTTP failure, a short/placeholder artifact, or a failed delivery-check verdict.

## 3. Evidence

Class A — executed locally on 2026-07-22:

```text
delivery page : HTTP 200, 3324 bytes
link limit    : 1
success URL   : https://one-honest-dollar.cloud-pyramid.workers.dev/ (match)
DELIVERY_CHECK: https://one-honest-dollar.cloud-pyramid.workers.dev/ | status=200 |
bytes=3324 | placeholder=none | sha256=n/a | link_limit=1 | redirect=match | verdict=PASS
```

Class E — [#39](https://github.com/ImmortalDemonGod/money-agent/issues/39) requires a real
test-mode delivery-seam exercise.

## 4. Limitations

This validates the configured success target without completing a card checkout. The probe follows
#39's minimum acceptance path: fetch and validate the provider-configured success redirect.

## 5. Reproduction

Use a Stripe test-mode `STRIPE_WRITE_KEY`, then run:

```bash
python3 bin/delivery_check.py https://one-honest-dollar.cloud-pyramid.workers.dev/ --payment-link <test-link-url>
```
