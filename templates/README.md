# templates/ — the forms a run fills in

Copy to the repo root (dropping `.template`), fill with REAL evidence, commit. The gates check
the filled copies mechanically; an unfilled or placeholder copy fails closed.

| Template | Filled copy | Checked by | When you need it |
|---|---|---|---|
| `EXHAUSTION_PACKET.template.md` | `EXHAUSTION_PACKET.md` | `bin/conclusion_gate.py` layer 2 | before recording an "impossible" conclusion |
| `ADVERSARY_REPORT.template.md` | `ADVERSARY_REPORT.md` (+ `ADVERSARY_TRANSCRIPT.md`) | `bin/conclusion_gate.py` layer 3 | same — the fresh-context novelty check |
| `EDGE_REGISTRATION.template.md` | `EDGE_REGISTRATION.md` | `bin/edge.py register`, frozen by `bin/edge_pnl.py` | BEFORE acting on a paper-rail edge |

(The per-iteration packet template lives with the packets: `.github/aiv-packets/TEMPLATE.md`,
pre-filled by `bin/iter.py new`.)
