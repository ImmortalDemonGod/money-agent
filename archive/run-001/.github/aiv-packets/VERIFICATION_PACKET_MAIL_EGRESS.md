# AIV Verification Packet (v2.1)

**Commit:** `bin/mail.py` proxy tunnel + fail-fast; sandbox mail egress measured DEAD
**Protocol:** AIV v2.0 + Addendum 2.7

## Classification (required)

```yaml
classification:
  risk_tier: R3
  sod_mode: S1
  critical_surfaces: [autonomous_execution, reputation, experiment_validity]
  blast_radius: "No mail can leave or reach this sandbox. The largest unmitigated risk (real-name
    sends) is mechanically foreclosed for this run; the distribution surface is correspondingly
    narrowed, which partially re-introduces the rig the unrig commit (2f078b8) removed. This packet
    exists so that narrowing is a documented fact at interpretation time, not a silent one."
  classification_rationale: "R3 inherited: touches the run's validity and the agent's largest
    capability. No money moved."
  classified_by: "agent (sandbox session, pre-run)"
  classified_at: "2026-07-16T08:45:00Z"
```

## Claim(s)

1. Email (IMAP 993, SMTP 587/465) **cannot work from this sandbox**: raw connects hang (SYN
   black-holed) and the HTTPS proxy answers CONNECT with `200 Connection Established` and then
   passes **zero bytes**.
2. `bin/mail.py` now **fails fast with a real error** in this environment instead of hanging until
   a harness timeout, and gains genuine proxy support for hosts whose proxies actually relay.
3. Off-sandbox behavior is unchanged (no `HTTPS_PROXY` -> direct socket, plus a 30s timeout).

## Evidence by class

| Class | Evidence |
|---|---|
| A (Execution) | `socket.connect` to imap.gmail.com:993 / smtp.gmail.com:587 / :465 -> `TimeoutError` (api.stripe.com:443 -> OK, same probe). Proxy `CONNECT imap.gmail.com:993` -> `HTTP/1.1 200` then TLS handshake -> `ConnectionResetError 104`. `CONNECT smtp.gmail.com:587` -> `200` then plaintext banner never arrives (`SMTPServerDisconnected: timed out`). |
| C (Negative) | Control: `CONNECT api.stripe.com:443` through the SAME proxy completes a real TLSv1.3 handshake -> the mail failure is port policy, not proxy breakage. **Nothing was sent** during any probe; SMTP never reached AUTH. Off-sandbox path unchanged by inspection: `_tunnel()` returns `socket.create_connection` verbatim when `HTTPS_PROXY` is unset. |
| B (Referential) | `bin/mail.py`: `_tunnel()`, `_ProxyIMAP4_SSL`, `_ProxySMTP`; `_imap()` and `send()` now construct the proxied variants. This commit. |
| D (Differential) | Before: `bin/mail.py inbox` hung 120s until killed by the harness, no error text. After: fails in seconds with `ConnectionResetError`/`OSError` naming the proxy. Capability matrix: prompt says read+send; this sandbox delivers neither. |
| E (Intent) | PROMPT.md and CONSTITUTION.md grant email as a capability; EMAIL_AND_UNRIG added it so the run would not assume its own conclusion. This packet names the regression so the operator decides with eyes open rather than the run silently losing its distribution rail. |
| F (Provenance) | N/A -- no money claim is made, no ledger pull is cited, `received_usd` is untouched by this change; there is no hash for a network policy. The probes above are reproducible in one command each. |

## Cost

- Spent this iteration: 0 USD (nothing purchased; probes were free API/socket calls)

## Honest limitations

1. **The first CONNECT probe fooled the author.** It read the proxy's `200` and declared the
   tunnel viable; only driving a real handshake exposed the black-hole. Same trap as `aiv init`
   printing "Installed": the status line is a claim, the behavior is the fact.
2. The tunnel code's positive path (a proxy that genuinely relays mail ports) is **untested here**
   -- untestable in this sandbox by construction. It is exercised only up to the CONNECT phase.
3. Whether the run should proceed email-less is an **operator decision** this packet deliberately
   does not make.
