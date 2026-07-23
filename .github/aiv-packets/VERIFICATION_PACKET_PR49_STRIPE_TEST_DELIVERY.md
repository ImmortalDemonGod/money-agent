# AIV Verification Packet — PR49 Stripe Test Delivery

Author: ImmortalDemonGod
Verifier: Codex

## 0. Logical unit

External acceptance evidence for #39. A Stripe **test-mode** $1 product, Price, and Payment Link
were created with `restrictions.completed_sessions.limit=1` and a provider-configured completion
redirect to the dedicated static test artifact at
`https://money-agent-test-delivery.cloud-pyramid.workers.dev`.

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

CLM-001: The test Payment Link is provider-capped at one completed session, completed a Stripe
test-mode card checkout, and its configured success redirect serves a complete explicitly typed
public artifact. Falsified by a non-1 limit, incomplete/unpaid session, redirect mismatch, HTTP
failure, missing/non-document content type, a short/placeholder artifact, or a failed
delivery-check verdict.

## 3. Evidence

Class A — executed locally on 2026-07-22 after completing the hosted Stripe test-mode checkout:

```text
Checkout Session: status=complete, payment_status=paid, mode=payment, livemode=false
Payment Link: completed_sessions.count=1, completed_sessions.limit=1, active=false
Checkout success_url: https://money-agent-test-delivery.cloud-pyramid.workers.dev
delivery page : HTTP 200, 378 bytes
content type  : text/plain
link limit    : 1
success URL   : https://money-agent-test-delivery.cloud-pyramid.workers.dev (match)
DELIVERY_CHECK: https://money-agent-test-delivery.cloud-pyramid.workers.dev | status=200 |
bytes=378 | content_type=text/plain | placeholder=none | sha256=n/a | link_limit=1 |
redirect=match | verdict=PASS
```

Class E — [#39](https://github.com/ImmortalDemonGod/money-agent/issues/39) requires a real
test-mode delivery-seam exercise.

## 4. Limitations

This is a disposable sandbox fixture: it has no live-mode credentials, customer data, or storefront
rendering. The completed link is intentionally inactive after its one permitted test session;
future runs must provision a new fixture rather than weaken the cap.

## 5. Reproduction

Use a Stripe test-mode `STRIPE_WRITE_KEY`, then run:

```bash
python3 bin/delivery_check.py https://money-agent-test-delivery.cloud-pyramid.workers.dev --payment-link <test-link-url>
```
